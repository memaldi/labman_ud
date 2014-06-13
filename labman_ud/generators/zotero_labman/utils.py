# -*- coding: utf-8 -*-

from django.template.defaultfilters import slugify

from django.conf import settings
from django.utils.timezone import utc
from django.core.mail import send_mail

from generators.zotero_labman.models import ZoteroLog
from entities.events.models import Event, EventType
from entities.publications.models import Publication, PublicationType, PublicationAuthor, PublicationTag
from entities.organizations.models import Organization, OrganizationType
from entities.utils.models import Language, Tag
from entities.persons.models import Person, Nickname, Job
from entities.projects.models import Project, RelatedPublication, ProjectTag
from entities.news.models import PublicationRelatedToNews, NewsTag

from pyzotero import zotero
from dateutil import parser
from datetime import datetime, date

import requests
import os
import re
import logging
import json
import operator
import difflib
import itertools

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Dict with supported Zotero itemTypes, translated to LabMan's PublicationTypes
SUPPORTED_ITEM_TYPES = {
    'bookSection': 'Book section',
    'book': 'Book',
    'journalArticle': 'Journal article',
    'magazineArticle': 'Magazine article',
    'newspaperArticle': 'Newspaper article',
    'thesis': 'PhD thesis',
    'report': 'Technical Report',
    'patent': 'Misc',
    'presentation': 'Misc',
    'document': 'Misc',
    'conferencePaper': 'Conference paper',
}


# Dict used for tag dissambiguation
tag_nicks = {
    'AAL': 'Ambient Assisted Living',
    'ambient assisted living environments': 'Ambient Assisted Living',
    'assisted living': 'Ambient Assisted Living',
    'assistive': 'Ambient Assisted Living',
    'ambient assisted citizens': 'ambient assisted cities',
    'Artificial Intelligence (incl. Robotics)': 'Artificial Intelligence',
    'Computational Intelligence': 'Artificial Intelligence',
    'Computation by Abstract Devices': 'Artificial Intelligence',
    'bayesian network': 'Bayesian Networks',
    'client-server system': 'client-server systems',
    'content creation; user centered design contextual design': 'Content Creation',
    'context-aware': 'Context-Aware Computing',
    'context-aware development toolkits': 'Context-Aware Computing',
    'context-awareness': 'Context-Aware Computing',
    'context-aware services development': 'Context-Aware Computing',
    'context-aware system development': 'Context-Aware Computing',
    'context-aware systems': 'Context-Aware Computing',
    'context data management': 'Context-Aware Computing',
    'context data sources': 'Context-Aware Computing',
    'context management': 'Context-Aware Computing',
    'Context modeling': 'context modelling',
    'contextual design': 'Context-Aware Computing',
    'data handling': 'Data Management',
    'dispositivos móviles': 'Mobile Devices',
    'domain expert': 'domain experts',
    'Domotic': 'Domotics',
    'domotics': 'Domotics',
    'Educational programs': 'Educational Technologies',
    'educational technology': 'Educational Technologies',
    'elderly': 'Elderly People',
    'Elders': 'Elderly People',
    'Embedded': 'Embedded Devices',
    'emergency detection': 'Emergency Management',
    'evaluación': 'Evaluation',
    'experiencia del usuario': 'User Experience',
    'first-order didactic resource': 'Educational Technologies',
    'Fuzzy': 'Fuzzy Logic',
    'gestión de energía': 'Energy Management',
    'Grid Services': 'Grid',
    'hci': 'Human Computer Interaction',
    'Information Systems Applications (incl.Internet)': 'Information Systems Applications',
    'Information Systems Applications (incl. Internet)': 'Information Systems Applications',
    'inference': 'inference mechanisms',
    'IoT': 'Internet of Things',
    'learning': 'Educational Technologies',
    'Opinion Minning': 'opinion mining',
    'Persuasive Technologies': 'persuasive technology',
    'reasoners': 'Reasoning Engines',
    'Recomendation Systems': 'Recommendation Systems',
    'seguridad': 'Security',
    'semantic': 'Semantic Technologies',
    'Semantic reasoners': 'Semantic Inference',
    'semantic reasoning': 'Semantic Inference',
    'Semantics': 'Semantic Technologies',
    'servicios móviles': 'Mobile Services',
    'Smart everyday objects': 'Smart Everyday Object',
    'smart phones': 'smartphones',
    'social content sharing': 'Social Data Mining',
    'software design': 'Software Engineering',
    'triple space': 'triple space computing',
    'triple space computing paradigm': 'triple space computing',
    'triplespaces': 'triple space computing',
    'ubiquitous': 'ubiquitous computing',
    'uncertainty': 'Uncertainty Reasoning',
    'wearable computers': 'Wearable Computing'
}


def dissambiguate(tag):
    correct_tag = tag
    if tag in tag_nicks.keys():
        correct_tag = tag_nicks[tag]
    return correct_tag


def get_zotero_variables():
    # TODO: Check variables
    api_key = getattr(settings, 'ZOTERO_API_KEY', None)
    library_id = getattr(settings, 'ZOTERO_LIBRARY_ID', None)
    library_type = getattr(settings, 'ZOTERO_LIBRARY_TYPE', None)
    api_limit = 10

    return api_key, library_id, library_type, api_limit


#gets the max id of all the items in the library, taking into account both the items and the trash
def get_last_zotero_version():
    api_key, library_id, library_type, api_limit = get_zotero_variables()

    r = requests.get('https://api.zotero.org/' + library_type + 's/' + library_id + '/items?format=versions&key=' + api_key)
    if len(r.json()):
        max_items = max(r.json().items(), key=operator.itemgetter(1))[1]
    else:
        max_items = 0

    r = requests.get('https://api.zotero.org/' + library_type + 's/' + library_id + '/items/trash?format=versions&key=' + api_key)
    if len(r.json()):
        max_trash = max(r.json().items(), key=operator.itemgetter(1))[1]
    else:
        max_trash = 0

    return max(max_items, max_trash)


def parse_last_items(last_version, version=0, prefix='[NEW_ITEMS_SYNC]'):
    api_key, library_id, library_type, api_limit = get_zotero_variables()

    zot = zotero.Zotero(library_id, library_type, api_key)

    # Dataset of backed up info from deleted publications
    backup_dataset = []

    if version == last_version:
        logger.info('Labman is already updated to last version in Zotero (%i)! :-)' % (last_version))
    else:
        if version > last_version:
            # This should not happend anytime, but in this case, we solve the error by syncing the penultimate version in Zotero
            logger.info('Labman version number (%i) is higher than Zotero\'s one (%i)... :-/ Solving the error...' % (version, last_version))
            version = last_version - 1

        logger.info('Getting items since version %i' % (version))
        logger.info('Last version in Zotero is %i' % (last_version))

        gen = zot.makeiter(zot.items(limit=api_limit, order='dateModified', sort='desc', newer=version))

        lastitems = []

        moreitems = True
        while moreitems:
            try:
                items = gen.next()
            except StopIteration:
                moreitems = False

            if items and items != lastitems:
                for item in items:
                    if item['itemType'] in SUPPORTED_ITEM_TYPES:
                        # Delete publication if exists
                        pub = None
                        try:
                            pub = ZoteroLog.objects.filter(zotero_key=item['key']).order_by('-created')[0].publication
                        except:
                            try:
                                pub = Publication.objects.get(slug=slugify(str(item['title'].encode('utf-8'))))
                            except:
                                pass

                        if pub:
                            logger.info('Item already exists! Deleting...')
                            backup_data = None
                            backup_data = delete_publication(pub)
                            if backup_data:
                                backup_dataset.extend(backup_data)

                        # Create new publication
                        logger.info('Creating new publication: %s' % (item['title']))
                        pub = None
                        pub, authors, tags, tag_project_rels, observations = get_publication_details(item)
                        if observations:
                            logger.info('Saved but... %s' % (observations))

                        logger.info('Saving publication...')

                        # Save publication
                        pub.save()

                        # Saving authors and tags (many-to-many fields)
                        logger.info('Saving authors and tags...')

                        order = 1
                        for author in authors:
                            pubauth = PublicationAuthor(
                                author=author,
                                publication=pub,
                                position=order
                            )
                            pubauth.save()
                            order += 1
                        for tag in tags:
                            pubtag = PublicationTag(
                                publication=pub,
                                tag=tag
                            )
                            pubtag.save()
                        for tag in tag_project_rels:
                            logger.info('Saving found publication-project relationship: %s' % (tag))
                            try:
                                pubproj = RelatedPublication(publication=pub, project=Project.objects.get(slug=tag))
                                pubproj.save()
                            except:
                                logger.info('Unable to create the relationship :-/')

                        # Save log
                        zotlog = ZoteroLog(zotero_key=item['key'], updated=parser.parse(item['updated']), version=last_version, observations=observations)
                        zotlog.publication = pub
                        zotlog.save()
                        logger.info('OK!')

                        logger.info('-'*30)
                lastitems = items
        # Generate a log specifying that the sync has finished for X version (due to avoid synchronization errors)
        zotlog = ZoteroLog(zotero_key='-SYNCFINISHED-', updated=datetime.utcnow().replace(tzinfo=utc), version=last_version, observations='')
        zotlog.save()

        # Restore news of deleted items, if any
        logger.info('Restoring news of deleted items, if any')
        restore_news(backup_dataset)


def check_what_is_missing(last_version, prefix='[CHECK_MISSING]'):
    api_key, library_id, library_type, api_limit = get_zotero_variables()

    zot = zotero.Zotero(library_id, library_type, api_key)

    gen = zot.makeiter(zot.items(limit=api_limit, order='dateModified', sort='desc', newer=0))

    lastitems = []
    item_set = set()

    moreitems = True
    while moreitems:
        try:
            items = gen.next()
        except StopIteration:
            moreitems = False

        if items and items != lastitems:
            for item in items:
                if item['itemType'] in ['attachment', 'note']:
                    pass
                elif item['itemType'] not in SUPPORTED_ITEM_TYPES:
                    logger.info('Item not in supported types...')
                    logger.info(item['itemType'])
                else:
                    pub = None
                    try:
                        pub = ZoteroLog.objects.filter(zotero_key=item['key']).order_by('-created')[0].publication
                    except:
                        try:
                            pub = Publication.objects.get(slug=slugify(str(item['title'].encode('utf-8'))))
                        except:
                            pass

                    if not pub:
                        logger.info('Item doesn\'t exist...')
                        item_set.add(item['title'])
            lastitems = items

    logger.info('-'*40)
    logger.info(item_set)
    logger.info(len(item_set))
    logger.info('-'*40)


def sync_deleted_items(last_version, version, prefix='[DELETE_SYNC]'):
    api_key, library_id, library_type, api_limit = get_zotero_variables()

    zot = zotero.Zotero(library_id, library_type, api_key)

    if version == last_version:
        logger.info('Labman is already updated to last version in Zotero (%i)! :-)' % (last_version))
    else:
        if version > last_version:
            # This should not happend anytime, but in this case, we solve the error by syncing the penultimate version in Zotero
            logger.info('Labman version number (%i) is higher than Zotero\'s one (%i)... :-/ Solving the error...' % (version, last_version))
            version = last_version - 1

        logger.info('Getting removed items since version %i' % (version))
        logger.info('Last version in Zotero is %i' % (last_version))
        logger.info('\n')

        gen = zot.makeiter(zot.trash(limit=api_limit, order='dateModified', sort='desc', newer=version))

        lastitems = []

        moreitems = True
        while moreitems:
            try:
                items = gen.next()
            except StopIteration:
                moreitems = False

            if items and items != lastitems:
                for item in items:
                    if item['itemType'] in SUPPORTED_ITEM_TYPES:
                        try:
                            pub = ZoteroLog.objects.filter(zotero_key=item['key']).order_by('-created')[0].publication
                            logger.info('Deleting %s...' % (item['title']))

                            delete_publication(pub)

                            zotlog = ZoteroLog(zotero_key=item['key'], updated=parser.parse(item['updated']), version=last_version, delete=True, publication=None)
                            zotlog.save()
                            logger.info('-'*30)
                        except:
                            pass
                lastitems = items
        # Generate a log specifying that the sync has finished for X version (due to avoid synchronization errors)
        zotlog = ZoteroLog(zotero_key='-SYNCFINISHED-', updated=datetime.utcnow().replace(tzinfo=utc), version=last_version, delete=True, observations='')
        zotlog.save()


def get_publication_details(item):
    pub = Publication()

    observations = ''

    # Publicaton type
    pub.publication_type, created = PublicationType.objects.get_or_create(name=SUPPORTED_ITEM_TYPES[item['itemType']])

    # Publication language
    if 'language' in item and item['language']:
        pub.language, created = Language.objects.get_or_create(
            slug=slugify(str(item['language'].encode('utf-8'))),
            defaults={'name': item['language']}
        )
    else:
        pub.language = None

    # Publication date / year
    try:
        pub.published = parser.parse(item['date'])
        pub.year = pub.published.year
    except:
        year = re.findall(r'\d{4}', item['date'])
        if year:
            pub.published = datetime(int(year[0]), 1, 1)
            pub.year = year[0]
        else:
            pub.published = None
            pub.year = '2030'
            error_msg = 'Error getting year from %s.' % (str(item['date']))
            logger.error(error_msg)
            observations = error_msg

    # University
    if 'university' in item and item['university']:
        organization_type, created = OrganizationType.objects.get_or_create(name='University')
        pub.university, created = Organization.objects.get_or_create(
            slug=slugify(str(item['university'].encode('utf-8'))),
            defaults={'organization_type': organization_type, 'full_name': item['university']}
        )

    # Common attributes for all publications
    pub.title = item['title']
    pub.abstract = item['abstractNote']
    pub.short_title = item['shortTitle'] if 'shortTitle' in item and item['shortTitle'] else None
    pub.doi = item['DOI'] if 'DOI' in item and item['DOI'] else None
    pub.pages = item['pages'] if 'pages' in item and item['pages'] else None
    pub.issue = item['issue'] if 'issue' in item and item['issue'] else None
    pub.book_title = item['bookTitle'] if 'bookTitle' in item and item['bookTitle'] else None

    # Attributes that can be both from publications and "parent" publications
    pub_subpub_attributes = {
        'journal_abbreviation': item['journalAbbrevation'] if 'journalAbbrevation' in item and item['journalAbbrevation'] else None,
        'series': item['series'] if 'series' in item and item['series'] else None,
        'series_number': item['seriesNumber'] if 'seriesNumber' in item and item['seriesNumber'] else None,
        'volume': item['volume'] if 'volume' in item and item['volume'] else None,
        'publisher': item['publisher'] if 'publisher' in item and item['publisher'] else None,
        'edition': item['edition'] if 'edition' in item and item['edition'] else None,
        'series_text': item['seriesText'] if 'seriesText' in item and item['seriesText'] else None,
        'isbn': item['ISBN'] if 'ISBN' in item and item['ISBN'] else None,
        'issn': item['ISSN'] if 'ISSN' in item and item['ISSN'] else None,
        'year': pub.year,
    }

    # If conference paper, create Conference event and Proceeding parent publication
    if item['itemType'] == 'conferencePaper':
        if item['conferenceName']:
            conf_name = item['conferenceName']
        else:
            conf_name = item['proceedingsTitle']
            conf_name = conf_name.replace('proc. of the ', '')
            conf_name = conf_name.replace('Proc. of the ', '')
            conf_name = conf_name.replace('proceedings of the ', '')
            conf_name = conf_name.replace('Proceedings of the ', '')

        proceedings_title = item['proceedingsTitle'] if item['proceedingsTitle'] else 'Proceedings of ' + conf_name

        pub_type_proceedings, created = PublicationType.objects.get_or_create(name='Proceedings')

        pub_subpub_attributes['abstract'] = proceedings_title
        pub_subpub_attributes['title'] = proceedings_title
        pub_subpub_attributes['publication_type'] = pub_type_proceedings

        proceedings, created = Publication.objects.get_or_create(
            slug=slugify(str(proceedings_title.encode('utf-8'))),
            defaults=pub_subpub_attributes
        )

        if proceedings.publication_type != pub_type_proceedings:
            proceedings.publication_type = pub_type_proceedings
            proceedings.save()

        event_type_academic, created = EventType.objects.get_or_create(name='Academic event')
        pub.presented_at, created = Event.objects.get_or_create(
            slug=slugify(str(conf_name.encode('utf-8'))),
            defaults={
                'full_name': conf_name,
                'event_type': event_type_academic,
                'year': pub.published.year,
                'location': item['place'],
                'proceedings': proceedings
            }
        )

        # Relation between the publication and its parent
        pub.part_of = proceedings

    # If journal, magazine or newspaper article or book section, create parent publication
    elif item['itemType'] in ['bookSection', 'journalArticle', 'magazineArticle', 'newspaperArticle']:
        if item['itemType'] == 'bookSection':
            parentpub_type, created = PublicationType.objects.get_or_create(name='Book')
            parentpub_title = item['bookTitle'] if 'bookTitle' in item and item['bookTitle'] else 'Book ?'
        elif item['itemType'] == 'journalArticle':
            parentpub_type, created = PublicationType.objects.get_or_create(name='Journal')
            parentpub_title = item['publicationTitle'] if 'publicationTitle' in item and item['publicationTitle'] else None
            if not parentpub_title:
                parentpub_title = item['journal_abbreviation'] if 'journalAbbrevation' in item and item['journalAbbrevation'] else 'Journal ?'
        elif item['itemType'] == 'magazineArticle':
            parentpub_type, created = PublicationType.objects.get_or_create(name='Magazine')
            parentpub_title = item['publicationTitle'] if 'publicationTitle' in item and item['publicationTitle'] else 'Magazine ?'
        elif item['itemType'] == 'newspaperArticle':
            parentpub_type, created = PublicationType.objects.get_or_create(name='Newspaper')
            parentpub_title = item['publicationTitle'] if 'publicationTitle' in item and item['publicationTitle'] else 'Newspaper ?'

        pub_subpub_attributes['abstract'] = ' '
        pub_subpub_attributes['title'] = parentpub_title
        pub_subpub_attributes['publication_type'] = parentpub_type

        parentpub, created = Publication.objects.get_or_create(
            slug=slugify(str(parentpub_title.encode('utf-8'))),
            defaults=pub_subpub_attributes
        )

        if parentpub.publication_type != parentpub_type:
            parentpub.publication_type = parentpub_type
            parentpub.save()

        # Relation between the publication and its parent
        pub.part_of = parentpub

    # If it has no parent publication, all those attributes go to publication itself
    else:
        pub.__dict__.update(pub_subpub_attributes)

    # Get PDF attachments

    # Determine pdf path...
    # ...if the publication is presented at any event (conference, workshop, etc.), it will be stored like:
    #   publications/2012/ucami/title-of-the-paper.pdf
    # ...otherwise, it will be stored like:
    #   publications/2012/book-chapter/title-of-the-paper.pdf
    if pub.presented_at:
        sub_folder = pub.presented_at.slug
    else:
        sub_folder = pub.publication_type.slug
    pdf_path = '%s/%s/%s/%s' % ('publications', pub.year, sub_folder, slugify(str(pub.title.encode('utf-8'))) + '.pdf')

    has_attachment = get_attached_pdf(item['key'], pdf_path)
    if has_attachment:
        pub.pdf = pdf_path

    # Get bibtex
    pub.bibtex = get_bibtex(item['key'])

    # Authors
    # We save them later (when we save pub in DB) (many-to-many fields)
    authors = []
    for creator in item['creators']:
        if creator['creatorType'] == 'author':
            author_name = ''
            if 'name' in creator and creator['name']:
                author_name = str(creator['name'].encode('utf-8'))
                first_surname = author_name.split(' ')[-1]
                first_name = author_name.replace(' ' + first_surname, '')

            first_name = str(creator['firstName'].encode('utf-8')) if 'firstName' in creator and creator['firstName'] else 'John'
            first_surname = str(creator['lastName'].encode('utf-8')) if 'lastName' in creator and creator['lastName'] else 'Doe'

            if not author_name:
                author_name = '%s %s' % (first_name, first_surname)

            author_slug = slugify(author_name)
            try:
                # Check if author is in DB (comparing by slug)
                a = Person.objects.get(slug=author_slug)
            except:
                # If it isn't
                try:
                    # Check if author name correspond with any of the posible nicknames of the authors in DB
                    nick = Nickname.objects.get(slug=slugify(author_name))
                    a = nick.person
                except:
                    # If there is no reference to that person in the DB, create a new one
                    a = Person(
                        first_name=first_name,
                        first_surname=first_surname
                    )
                    a.save()
                    # TODO: Send email to admins notifying the creation of new person
            authors.append(a)

    # Tags
    tags = []
    tag_project_rels = []

    # Get the slugs of all the projects in labman to create pub-proj relationships (based on tag comparision)
    project_slugs = [slug['slug'] for slug in Project.objects.all().order_by('slug').values('slug')]

    for tag in item['tags']:
        try:
            tag_str = str(tag['tag'].encode('utf-8'))
            tag_str = dissambiguate(tag_str).lower()
            tag_slug = slugify(tag_str)

            # Check if the publication has the 'jcrX.XXX' tag including the impact factor of the publication
            jcr_pattern = r'(jcr|if)(\d(\.|\,)\d+)'
            jcr_match = re.match(jcr_pattern, tag_str)
            if jcr_match:
                impact_factor = jcr_match.groups()[1]
                if jcr_match.groups()[2] == ',':
                    impact_factor = impact_factor.replace(',', '.')
                if parentpub:
                    parentpub.impact_factor = float(impact_factor)
                    parentpub.save()
                else:
                    pub.impact_factor = float(impact_factor)
            elif tag_slug in project_slugs:
                # Find publication - project relations through tags
                tag_project_rels.append(tag_slug)
            else:
                # If it doesn't, create the tag as normal
                if len(tag['tag']) <= 75:
                    t, created = Tag.objects.get_or_create(
                        slug=tag_slug,
                        defaults={'name': tag_str}
                    )
                    tags.append(t)
        except:
            pass

    return pub, authors, tags, tag_project_rels, observations


def get_attached_pdf(item_key, path):
    api_key, library_id, library_type, api_limit = get_zotero_variables()

    zot = zotero.Zotero(library_id, library_type, api_key)
    children = zot.children(item_key)

    for child in children:
        # Finde if there is any attached PDF
        if child['itemType'] == 'attachment' and child['contentType'] == 'application/pdf':
            logger.info('Getting attachment: ' + child['filename'] + '...')

            r = requests.get('https://api.zotero.org/' + library_type + 's/' + library_id + '/items/' + child['key'] + '/file?key=' + api_key)

            # If the directory doesn't exist, create it
            pdf_dir = getattr(settings, 'MEDIA_ROOT', None) + '/' + os.path.dirname(path)
            if not os.path.exists(pdf_dir):
                os.makedirs(pdf_dir)

            with open(getattr(settings, 'MEDIA_ROOT', None) + '/' + path, 'wb') as pdffile:
                pdffile.write(r.content)

            return True

    return False


def get_bibtex(item_key):
    api_key, library_id, library_type, api_limit = get_zotero_variables()

    zot = zotero.Zotero(library_id, library_type, api_key)
    bibtex = zot.item(item_key, content='bibtex')
    return ''.join(bibtex)


def delete_publication(pub):
    # We return a list of backup dicts, of the publication and its children
    ret_list = []

    try:
        zot_key = ZoteroLog.objects.filter(publication=pub).order_by('-created')[0].zotero_key
    except IndexError:
        zot_key = None

    publ_proj = set()
    if pub.projects.all():
        for proj in pub.projects.all():
            publ_proj.add(proj)

    # I don't understand why publ_news = pub.news.all() doesn't work as expected: the ret_dict is
    # generated correctly -with a list of news-, but when returned the list appears empty :-?
    publ_news = set()
    if pub.news.all():
        for nw in pub.news.all():
            publ_news.add(nw)

    # Create restored data dictionary
    ret_dict = {
        'zot_key': zot_key,
        'publ_event': pub.presented_at,
        'publ_lang': pub.language,
        'publ_observations': pub.observations,
        'publ_uni': pub.university,
        'publ_parentpub': pub.part_of,
        'publ_proj': publ_proj,
        'publ_news': publ_news,
    } if zot_key else None

    if ret_dict:
        ret_list.append(ret_dict)

    # Delete PDF file
    if pub.pdf:
        try:
            os.remove(getattr(settings, 'MEDIA_ROOT', None) + '/' + str(pub.pdf))
        except:
            pass

    # Check and backup if it has any children before deleting it (otherwise they will be deleted without backing up)
    for part in pub.has_part.all():
        backup_data = None
        backup_data = delete_publication(part)
        if backup_data:
            ret_list.extend(backup_data)

    # Delete publication object
    pub.delete()

    return ret_list


def correct_nicks():
    for nick in Nickname.objects.all():
        try:
            bad_person = Person.objects.get(slug=nick.slug)

            if bad_person and bad_person != nick.person:
                logger.info('Deleting... %s' % bad_person.full_name)
                for pubauth in PublicationAuthor.objects.filter(author=bad_person):
                    logger.info('Changing authorship of %s' % pubauth.publication)
                    pubauth.author = nick.person
                    pubauth.save()
                bad_person.delete()
        except:
            pass


def restore_news(backup_dataset):
    for pub_backup in backup_dataset:
        pub = None
        try:
            pub = ZoteroLog.objects.filter(zotero_key=pub_backup['zot_key']).order_by('-created')[0].publication
        except:
            pass

        if pub:
            for nw in pub_backup['publ_news']:
                logger.info('Restoring %s - %s...' % (pub, nw))
                pn = PublicationRelatedToNews()
                pn.publication = pub
                pn.news = nw
                pn.save()

    logger.info('OK!')
    logger.info('-'*30)


###########################################################################
# def: remove_unrelated_persons()
###########################################################################

def remove_unrelated_persons():
    unused_person_ids = set()
    organization_slugs = ['morelab', 'deustotech-internet', 'deustotech-telecom']

    all_persons = Person.objects.all()
    own_organizations = Organization.objects.filter(slug__in=organization_slugs)

    for person in all_persons:
        publications = person.publications.all()
        projects = person.projects.all()
        if (len(publications) == 0) and (len(projects) == 0):
            unused_person_ids.add(person.id)

    unused_persons = Person.objects.filter(id__in=unused_person_ids, is_active=False)

    persons_to_remove = set()

    removed_objects = 0

    for person in unused_persons:
        jobs = Job.objects.filter(person=person, organization__in=own_organizations)
        if len(jobs) == 0:
            removed_objects += 1
            persons_to_remove.add(person)
            logger.info(' Person to be deleted: %s' % person.full_name)
            person.delete()

    logger.info('Removed %d items' % removed_objects)


def load_tag_nicks(path='tag_nicks.json'):
    nicks = json.load(open(path, 'r'))
    return nicks


###########################################################################
# def: remove_unrelated_tags()
###########################################################################

def remove_unrelated_tags():
    used_tag_ids = set()

    for item in PublicationTag.objects.all():
        used_tag_ids.add(item.tag.id)

    for item in ProjectTag.objects.all():
        used_tag_ids.add(item.tag.id)

    for item in NewsTag.objects.all():
        used_tag_ids.add(item.tag.id)

    unused_tags = Tag.objects.exclude(id__in=used_tag_ids)

    removed_objects = 0

    for tag in unused_tags:
        logger.info(' Tag to be deleted: %s' % tag.name)
        tag.delete()
        removed_objects += 1

    logger.info('Removed %d items' % removed_objects)


###########################################################################
# def: check_for_similar_names()
###########################################################################

def check_for_similar_names(threshold_ratio):
    logger.info('Checking for similar names...')
    logger.info('#' * 75)

    name_list = []

    persons = Person.objects.all()

    for person in persons:
        name_list.append(person.full_name)

    for test_name, testing_name in itertools.combinations(name_list, 2):
        ratio = difflib.SequenceMatcher(None, test_name, testing_name).ratio()

        if (ratio > threshold_ratio):
            logger.info('%f\t%s\t\t\tcould be\t\t\t%s' % (ratio, test_name, testing_name))


###########################################################################
# def: check_for_non_active_members()
###########################################################################

def check_for_non_active_members():
    logger.info('')
    logger.info('Checking for non active members...')
    logger.info('#' * 75)

    today = date.today()

    persons = Person.objects.filter(is_active=True)

    for person in persons:
        last_job = Job.objects.filter(person_id=person.id).order_by('-end_date')[0]
        if (last_job.end_date) and (last_job.end_date < today):
            logger.info('\t\t%s is no longer active' % person.full_name)
            person.is_active = False
            person.save()
            logger.info('\t\t%s\'s status changed to non-active' % person.full_name)


###########################################################################
# def: check_incomplete_project_dates_info()
###########################################################################

def check_incomplete_project_dates_info():
    logger.info('')
    logger.info('Checking for incomplete project dates info...')
    logger.info('#' * 75)

    projects_without_start_month = Project.objects.filter(start_month='')

    for project in projects_without_start_month:
        logger.info('\t\t%s has no start_month' % project.short_name)
        project.start_month = 1
        logger.info('\t\t%s\'s start_month set to 1 by default' % project.short_name)
        project.save()

    projects_without_end_month = Project.objects.filter(end_month='')

    for project in projects_without_end_month:
        logger.info('\t\t%s has no end_month' % project.short_name)
        project.end_month = 12
        logger.info('\t\t%s\'s end_month set to 12 by default' % project.short_name)
        project.save()


###########################################################################
# def: greet_birthday()
###########################################################################

def greet_birthday():
    logger.info('')
    logger.info('Checking for members birthdays...')
    logger.info('#' * 75)

    members = Person.objects.filter(is_active=True)

    for member in members:
        birth_date = member.birth_date
        if birth_date:
            today = date.today()

            if (birth_date.day == today.day) and (birth_date.month == today.month):
                logger.info('\t\tToday is %s\'s birthday!' % member.full_name)
                try:
                    send_mail(
                        'Happy B-day %s... ;^)' % member.full_name,     # Subject
                        '¡Felicidades!\nZorionak!\nHappy birthday!',      # Message
                        getattr(settings, 'EMAIL_SENDER_ADDRESS', ''),  # From
                        getattr(settings, 'GENERAL_NOTIFICATIONS_ADDRESSES', []),   # To
                        fail_silently=False
                    )
                except:
                    logger.info('\t\tUnable to send e-mail')
