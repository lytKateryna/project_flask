from flask import Blueprint, jsonify, request
from pydantic import ValidationError
from sqlalchemy import select

from core.db import db
from models.categories import Category
from schemas.categories import (
    CategoryBase,
    CategoryCreateRequest,
    CategoryUpdateRequest,
)

category_bp = Blueprint(
    "category",
    __name__,
    url_prefix="/categories"
)


@category_bp.get("")
def get_all_categories():
    stmt = select(Category)
    categories = db.session.execute(stmt).scalars().all()

    response = [
        CategoryBase.model_validate(category).model_dump()
        for category in categories
    ]

    return jsonify(response), 200


@category_bp.post("")
def create_new_category():
    raw_data = request.get_json(silent=True)

    if not raw_data:
        return jsonify({"error": "Request body is missing or not valid JSON"}), 400

    try:
        validated_data = CategoryCreateRequest.model_validate(raw_data)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    try:
        new_category = Category(**validated_data.model_dump())

        db.session.add(new_category)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": "Failed to create new category",
            "detail": str(e)
        }), 500

    return jsonify(
        CategoryBase.model_validate(new_category).model_dump()
    ), 201


@category_bp.put("/<int:category_id>")
@category_bp.patch("/<int:category_id>")
def update_category_by_id(category_id: int):
    raw_data = request.get_json(silent=True)

    if not raw_data:
        return jsonify({"error": "Request body is missing or not valid JSON"}), 400

    try:
        validated_data = CategoryUpdateRequest.model_validate(raw_data)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    stmt = select(Category).where(Category.id == category_id)
    category = db.session.execute(stmt).scalar_one_or_none()

    if category is None:
        return jsonify({"error": f"Category with ID {category_id} not found"}), 404

    try:
        for key, value in validated_data.model_dump(exclude_none=True).items():
            setattr(category, key, value)

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": f"Failed to update category with ID {category_id}",
            "detail": str(e)
        }), 500

    return jsonify(
        CategoryBase.model_validate(category).model_dump()
    ), 200


@category_bp.delete("/<int:category_id>")
def delete_category_by_id(category_id: int):
    stmt = select(Category).where(Category.id == category_id)
    category = db.session.execute(stmt).scalar_one_or_none()

    if category is None:
        return jsonify({"error": f"Category with ID {category_id} not found"}), 404

    try:
        db.session.delete(category)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": f"Failed to delete category with ID {category_id}",
            "detail": str(e)
        }), 500

    return "", 204