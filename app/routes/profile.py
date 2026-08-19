from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..extensions import db
from ..models import Address, Favorite, Restaurant

profile_bp = Blueprint("profile", __name__, url_prefix="/profile")


@profile_bp.get("/")
@login_required
def profile():
    addresses = Address.query.filter_by(user_id=current_user.id).order_by(Address.is_default.desc(), Address.id).all()
    favorites = Favorite.query.filter_by(user_id=current_user.id).all()
    return render_template("profile.html", addresses=addresses, favorites=favorites)


@profile_bp.post("/update")
@login_required
def update_profile():
    current_user.name = request.form.get("name", "").strip() or current_user.name
    current_user.phone = request.form.get("phone", "").strip()
    db.session.commit()
    flash("Profil mis à jour.", "success")
    return redirect(url_for("profile.profile"))


@profile_bp.post("/address")
@login_required
def add_address():
    label = request.form.get("label", "Domicile").strip()
    street = request.form.get("street", "").strip()
    postal_code = request.form.get("postal_code", "").strip()
    city = request.form.get("city", "").strip()
    if not all([label, street, postal_code, city]):
        flash("Tous les champs de l'adresse sont obligatoires.", "danger")
        return redirect(url_for("profile.profile"))
    make_default = request.form.get("is_default") == "1"
    if make_default:
        Address.query.filter_by(user_id=current_user.id).update({"is_default": False})
    db.session.add(Address(user_id=current_user.id, label=label, street=street, postal_code=postal_code,
                           city=city, instructions=request.form.get("instructions", "").strip(),
                           is_default=make_default))
    db.session.commit()
    flash("Adresse ajoutée.", "success")
    return redirect(url_for("profile.profile"))


@profile_bp.post("/address/<int:address_id>/default")
@login_required
def set_default(address_id):
    address = Address.query.filter_by(id=address_id, user_id=current_user.id).first_or_404()
    Address.query.filter_by(user_id=current_user.id).update({"is_default": False})
    address.is_default = True
    db.session.commit()
    flash("Adresse par défaut mise à jour.", "success")
    return redirect(url_for("profile.profile"))


@profile_bp.post("/address/<int:address_id>/delete")
@login_required
def delete_address(address_id):
    address = Address.query.filter_by(id=address_id, user_id=current_user.id).first_or_404()
    db.session.delete(address)
    db.session.commit()
    flash("Adresse supprimée.", "info")
    return redirect(url_for("profile.profile"))
