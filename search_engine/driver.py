import json

from utils.sql import get_session
from utils.sql.handlers import get_row
from utils.sql.models.course_video import CourseVideo
from utils.sql.models.course_unit import CourseUnit
from utils.sql.models.course_subsection import CourseSubsection
from utils.sql.models.course_section import CourseSection
from utils.sql.models.course import Course
from utils.sql.models.institution import Institution
from utils.sql.models.subject import Subject


from search_engine.english_nlp import tokenize, normalize_token, is_stopword
from search_engine.retrieval import retrieve_using_vector_model


def process_search(raw_query, limit=None):
    '''
    Merely uses the vector model and the "video_transcripts" collection
    '''
    tokens = tokenize(raw_query)
    normalized_tokens = [normalize_token(t) for t in tokens]

    if normalized_tokens:
        collection = "video_transcripts"
        non_stopwords = [t for t in normalized_tokens if not is_stopword(t)]
        video_ids = retrieve_using_vector_model(collection, non_stopwords, limit)

        session = get_session()
        all_videos_data = [assemble_video_data(session, v) for v in video_ids]
        session.close()

        return json.dumps({
            "query" : raw_query,
            "count" : len(all_videos_data),
            "videos" : all_videos_data
        })
    else:
        return "No results found for query = '%s'" % raw_query


def assemble_video_data(session, video_id):
    '''
    Provided the ID of a video in the database, obtain additional
    data pertaining to it and return it as a dictionary.
    '''
    video = get_row(session, CourseVideo, CourseVideo.id, video_id)

    unit_id = session.query(CourseUnit.id).filter(\
        CourseUnit.videos.any(CourseVideo.id == video.id)).first()

    subsection_id = session.query(CourseSubsection.id).filter(\
        CourseSubsection.units.any(CourseUnit.id == unit_id))

    section_id = session.query(CourseSection.id).filter(\
        CourseSection.subsections.any(CourseSubsection.id == subsection_id))

    course = session.query(Course).filter(\
        Course.sections.any(CourseSection.id == section_id)).first()

    institutions = session.query(Institution).filter(\
        Institution.courses.any(Course.id == course.id))


    video_data = {
        "href" : "https://www.youtube.com/watch?v=" + video.youtube_id,
        "course_name" : course.name,
        "course_href" : course.href,
        "institutions" : [i.name for i in institutions],
        "subjects" : [s.name for s in course.subjects],
        "transcript" : video.transcript,
        "youtube_stats": {
            "as_of" : str(video.stats_as_of),
            "views" : video.yt_views,
            "likes" : video.yt_likes,
            "dislikes" : video.yt_dislikes,
            "favorites" : video.yt_favorites,
            "comments" : video.yt_comments,
        },
    }
    return video_data
