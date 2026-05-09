from flask import Blueprint, jsonify, request
from unicodedata import category
from models.categories import Category
from sqlalchemy import select
from core.db import db
from schemas.categories import CategoryBase
from pydantic import ValidationError

category_bp = Blueprint(
    "category",
    __name__,  # questions.py
    url_prefix="/category"
)

# GET
@category_bp.route("")
def get_all_categories():
    stmt = select(Category)
    categories = db.session.execute(stmt).scalars()
    response = [
        CategoryBase.model_validate(obj).model_dump()
        for obj in categories
     ]
    return jsonify(response), 200

# POST
@category_bp.route("/create", methods=["POST"])
def create_new_category():
    raw_data = request.get_json(silent=True)

    # 2. Провести проверки, что данные есть, они валидны, все требуемые колонки указаны
    if not raw_data:
        return jsonify(
            {
                "error": "Request body is missing or not valid JSON"
            }
        ), 400  # 400 BAD REQUEST

    try:
        validated_data = CategoryBase.model_validate(raw_data)
    except ValidationError as e:
        return jsonify(
            {
                "error": e.errors()
            }
        ), 400

    try:
        # 3. Попытаться создать новый объект
        new_question = Category(**validated_data.model_dump())

        # 4. Добавить объект в сессию
        db.session.add(new_question)

        # 5. Применить изменения из сессии в Базу Данных
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify(
            {
                "error": "Failed to create new question",
                "detail": str(e)
            }
        ), 500  # 500 INTERNAL SERVER ERROR

    # 6. Вернуть ответ
    return jsonify(CategoryBase.model_validate(new_question).model_dump()), 201  # 201 CREATED

# PUT
@category_bp.route("/<int:category_id>/update", methods=["PUT", "PATCH"])
def update_category_by_id(category_id: int):
    # 1. Попытаться Получить сырые данные
    raw_data = request.get_json(silent=True)

    # 2. Провести проверки, что данные есть, они валидны, все требуемые колонки указаны
    if not raw_data:
        return jsonify(
            {
                "error": "Request body is missing or not valid JSON"
            }
        ), 400  # 400 BAD REQUEST

    try:
        validated_data = CategoryBase.model_validate(raw_data)
    except ValidationError as e:
        return jsonify(
            {
                "error": e.errors()
            }
        ), 400

    stmt = select(Category).where(Category.id == category_id)
    question = db.session.execute(stmt).one_or_none()

    if not question:
        return jsonify({"error": f"Question with ID {category_id} not found"})

    try:
        for key, value in validated_data.model_dump().items():
            setattr(question, key, value)

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": f"Failed to update question with ID {category_id}",
            "detail": str(e)
        }), 500  # 500 INTERNAL SERVER ERROR

    return jsonify(CategoryBase.model_validate(question).model_dump()), 200

# DELETE
@category_bp.route("/<int:category_id>/delete", methods=["DELETE"])
def delete_category_by_id(category_id: int):
    stmt = select(Category).where(Category.id == category_id)
    question = db.session.execute(stmt).one_or_none()

    if not question:
        return jsonify({"error": f"Question with ID {category_id} not found"})

    try:
        db.session.delete(question)
        db.session.commit()
    except Exception as e:
        db.session.rollback()

        return jsonify({
            "error": f"Failed to delete Question with ID {category_id}",
            "detail": str(e)
        }), 500

    return jsonify({"message": f"Question with ID {category_id} deleted successfully"}), 204  # 204 NO CONTENT

