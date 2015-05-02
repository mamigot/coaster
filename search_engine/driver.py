import json

from utils.sql import get_session
from utils.sql.handlers import get_row
from utils.sql.models.course_video import CourseVideo

from search_engine.english_nlp import tokenize, normalize_token
from search_engine.retrieval import retrieve_using_vector_model


def process_search(raw_query):
    '''
    Merely uses the vector model and the "video_transcripts" collection
    '''
    tokens = tokenize(raw_query)
    normalized_tokens = [normalize_token(t) for t in tokens]

    if normalized_tokens:
        collection = "video_transcripts"
        video_ids = retrieve_using_vector_model(collection, normalized_tokens)

        session = get_session()
        all_videos_data = [assemble_video_data(session, v) for v in video_ids]
        session.close()

        return json.dumps(all_videos_data)
    else:
        return "No results found for query = '%s'" % raw_query


def assemble_video_data(session, video_id):
    '''
    Provided the ID of a video in the database, obtain additional
    data pertaining to it and return it as a dictionary.
    '''
    video = get_row(session, CourseVideo, CourseVideo.id, video_id)
    video_data = {
        "href" : video.href,
        #"transcript": video.transcript,
        "youtube_stats": {
            #"_as_of" : video.stats_as_of,
            "views" : video.yt_views,
            "likes" : video.yt_likes,
            "dislikes" : video.yt_dislikes,
            "favorites" : video.yt_favorites,
            "comments" : video.yt_comments,
        }
    }
    return video_data
