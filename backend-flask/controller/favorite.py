from flask import Blueprint, session, request
from model.favorite import Favorite

favorite = Blueprint("favorite", __name__)


# 收藏文章接口
@favorite.route('/favorite', methods=['POST'])
def add_favorite():
    # if
    article_id = request.form.get('article_id')
    if session.get('isLogin') is None:
        return 'not-login'
    else:
        try:
            Favorite().insert_favorite(article_id)
            return 'favorite-pass'
        except:
            return 'favorite-fail'


# 取消收藏接口
@favorite.route('/favorite/<int:article_id>', methods=['DELETE'])
def cancel_favorite(article_id):
    try:
        Favorite().cancel_favorite(article_id)
        return 'cancel-pass'
    except:
        return 'cancel-fail'
