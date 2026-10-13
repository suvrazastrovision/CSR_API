from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    sort_field = request.args.get("sort")
    direction = request.args.get("direction", "asc")

    if sort_field is not None and sort_field not in ("title", "content"):
        return jsonify({"message": "Invalid sort field. Use 'title' or 'content'."}), 400
    if direction not in ("asc", "desc"):
        return jsonify({"message": "Invalid sort direction. Use 'asc' or 'desc'."}), 400

    posts = POSTS.copy()
    if sort_field is not None:
        posts.sort(key=lambda post: post[sort_field].casefold(), reverse=direction == "desc")
    return jsonify(posts)


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    title_query = request.args.get("title", "").casefold()
    content_query = request.args.get("content", "").casefold()

    matching_posts = [
        post for post in POSTS
        if title_query in post["title"].casefold()
        and content_query in post["content"].casefold()
    ]
    return jsonify(matching_posts)


@app.route('/api/posts', methods=['POST'])
def add_post():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"message": "Request body must be a JSON object."}), 400

    missing_fields = [field for field in ("title", "content") if field not in data]
    if missing_fields:
        return jsonify({"message": f"Missing required fields: {', '.join(missing_fields)}"}), 400

    post = {
        "id": max((existing_post["id"] for existing_post in POSTS), default=0) + 1,
        "title": data["title"],
        "content": data["content"],
    }
    POSTS.append(post)
    return jsonify(post), 201


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post = next((post for post in POSTS if post["id"] == post_id), None)
    if post is None:
        return jsonify({"message": f"Post with id {post_id} was not found."}), 404

    POSTS.remove(post)
    return jsonify({"message": f"Post with id {post_id} has been deleted successfully."}), 200


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    post = next((post for post in POSTS if post["id"] == post_id), None)
    if post is None:
        return jsonify({"message": f"Post with id {post_id} was not found."}), 404

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"message": "Request body must be a JSON object."}), 400

    for field in ("title", "content"):
        if field in data:
            post[field] = data[field]

    return jsonify(post), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
