# Backend/routes.py
from flask import Blueprint, jsonify, request
from Backend.models import db, User, Category, Question, History
from sqlalchemy import text

main = Blueprint('main', __name__)

# Health check
@main.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'OK'}), 200

# Get all categories
@main.route('/api/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    result = [{'id': c.id, 'name': c.name} for c in categories]
    return jsonify(result), 200

# Get questions by category ID
@main.route('/api/questions/<int:category_id>', methods=['GET'])
def get_questions(category_id):
    questions = Question.query.filter_by(category_id=category_id).all()
    result = [{'id': q.id, 'content': q.content, 'link': q.link} for q in questions]
    return jsonify(result), 200

# Get all questions with category name and link
@main.route('/api/questions', methods=['GET'])
def get_all_questions():
    sql = text("""
        SELECT questions.content, questions.link, categories.name AS category_name
        FROM questions
        JOIN categories ON questions.category_id = categories.id
    """)
    results = db.session.execute(sql).fetchall()
    questions = [{'content': row[0], 'link': row[1], 'category': row[2]} for row in results]
    return jsonify(questions), 200

# Search questions by keyword (case-insensitive)
@main.route('/api/questions/search', methods=['GET'])
def search_questions():
    keyword = request.args.get('keyword')
    if not keyword:
        return jsonify({'error': 'Keyword is required'}), 400

    sql = text("""
        SELECT questions.content, questions.link, categories.name AS category_name
        FROM questions
        JOIN categories ON questions.category_id = categories.id
        WHERE questions.content ILIKE :keyword
    """)
    results = db.session.execute(sql, {'keyword': f'%{keyword}%'}).fetchall()
    questions = [{'content': row[0], 'link': row[1], 'category': row[2]} for row in results]
    return jsonify(questions), 200

# Create new user (登录和注册都用这个)
@main.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({'error': 'Email is required'}), 400

    existing = User.query.filter_by(email=email).first()
    if existing:
        return jsonify({'message': 'User login success'}), 200

    user = User(email=email)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created'}), 201

# Add search history
@main.route('/api/history', methods=['POST'])
def add_history():
    data = request.get_json()
    user_email = data.get('email')
    search_query = data.get('search_query')

    if not user_email or not search_query:
        return jsonify({'error': 'Missing email or search_query'}), 400

    history = History(user_email=user_email, search_query=search_query)
    db.session.add(history)
    db.session.commit()
    return jsonify({'message': 'History recorded'}), 201

# Get search history by email
@main.route('/api/history/<email>', methods=['GET'])
def get_history(email):
    histories = History.query.filter_by(user_email=email).order_by(History.timestamp.desc()).all()
    result = [{'query': h.search_query, 'timestamp': h.timestamp.isoformat()} for h in histories]
    return jsonify(result), 200

# Get all categories with their questions
@main.route('/api/questions/all', methods=['GET'])
def get_all_categories_with_questions():
    categories = Category.query.all()
    result = []

    for c in categories:
        questions = Question.query.filter_by(category_id=c.id).all()
        question_list = [
            {
                'id': q.id,
                'content': q.content,
                'link': q.link
            } for q in questions
        ]
        result.append({
            'category_id': c.id,
            'category_name': c.name,
            'questions': question_list
        })

    return jsonify(result), 200