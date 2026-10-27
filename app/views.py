from flask import render_template
from flask_appbuilder import ModelView
from flask_appbuilder.fieldwidgets import Select2Widget
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_login import current_user
from wtforms import SelectField

from . import app, appbuilder, db
from .models import Categoria, Ingrediente, MovimientoInventario, Plato, Receta


# ---------------------------------------------------------------
# RECETAS (se muestran tambien dentro de cada Plato)
# ---------------------------------------------------------------
class RecetaView(ModelView):
    datamodel = SQLAInterface(Receta)

    label_columns = {
        "plato": "Plato",
        "ingrediente": "Ingrediente",
        "cantidad_necesaria": "Cantidad necesaria",
    }
    list_columns = ["plato", "ingrediente", "cantidad_necesaria"]
    add_columns = ["plato", "ingrediente", "cantidad_necesaria"]
    edit_columns = add_columns
    show_columns = add_columns
    search_columns = ["plato", "ingrediente"]


# ---------------------------------------------------------------
# MOVIMIENTOS DE INVENTARIO
# ---------------------------------------------------------------
TIPOS_MOVIMIENTO = [("ENTRADA", "Entrada"), ("SALIDA", "Salida")]


class MovimientoInventarioView(ModelView):
    datamodel = SQLAInterface(MovimientoInventario)

    label_columns = {
        "ingrediente": "Ingrediente",
        "usuario": "Usuario",
        "tipo": "Tipo",
        "cantidad": "Cantidad",
        "motivo": "Motivo",
        "fecha": "Fecha",
    }
    list_columns = ["fecha", "tipo", "ingrediente", "cantidad", "motivo", "usuario"]
    add_columns = ["ingrediente", "tipo", "cantidad", "motivo"]
    edit_columns = add_columns
    show_columns = ["fecha", "tipo", "ingrediente", "cantidad", "motivo", "usuario"]
    search_columns = ["ingrediente", "tipo", "fecha", "usuario"]
    base_order = ("fecha", "desc")

    add_form_extra_fields = {
        "tipo": SelectField("Tipo", choices=TIPOS_MOVIMIENTO, widget=Select2Widget())
    }
    edit_form_extra_fields = add_form_extra_fields

    def pre_add(self, item):
        # El usuario que registra el movimiento es el que inicio sesion
        item.usuario_id = current_user.id


# ---------------------------------------------------------------
# INGREDIENTES (muestra sus movimientos y recetas)
# ---------------------------------------------------------------
class IngredienteView(ModelView):
    datamodel = SQLAInterface(Ingrediente)
    related_views = [MovimientoInventarioView, RecetaView]

    label_columns = {
        "nombre": "Nombre",
        "categoria": "Categoria",
        "cantidad": "Cantidad",
        "unidad_medida": "Unidad de medida",
        "costo_unitario": "Costo unitario",
        "stock_minimo": "Stock minimo",
        "fecha_vencimiento": "Fecha de vencimiento",
        "activo": "Activo",
    }
    list_columns = [
        "nombre",
        "categoria",
        "cantidad",
        "unidad_medida",
        "costo_unitario",
        "stock_minimo",
        "fecha_vencimiento",
        "activo",
    ]
    add_columns = list_columns
    edit_columns = list_columns
    show_columns = list_columns
    search_columns = ["nombre", "categoria", "fecha_vencimiento", "activo"]
    base_order = ("nombre", "asc")


# ---------------------------------------------------------------
# CATEGORIAS (muestra sus ingredientes)
# ---------------------------------------------------------------
class CategoriaView(ModelView):
    datamodel = SQLAInterface(Categoria)
    related_views = [IngredienteView]

    label_columns = {
        "nombre": "Nombre",
        "descripcion": "Descripcion",
        "activo": "Activo",
    }
    list_columns = ["nombre", "descripcion", "activo"]
    add_columns = list_columns
    edit_columns = list_columns
    show_columns = list_columns
    search_columns = ["nombre", "activo"]
    base_order = ("nombre", "asc")


# ---------------------------------------------------------------
# PLATOS (muestra su receta)
# ---------------------------------------------------------------
class PlatoView(ModelView):
    datamodel = SQLAInterface(Plato)
    related_views = [RecetaView]

    label_columns = {
        "nombre": "Nombre",
        "descripcion": "Descripcion",
        "precio": "Precio",
        "activo": "Activo",
    }
    list_columns = ["nombre", "descripcion", "precio", "activo"]
    add_columns = list_columns
    edit_columns = list_columns
    show_columns = list_columns
    search_columns = ["nombre", "activo"]
    base_order = ("nombre", "asc")


# ---------------------------------------------------------------
# MENU
# ---------------------------------------------------------------
appbuilder.add_view(
    CategoriaView,
    "Categorias",
    icon="fa-tags",
    category="Inventario",
    category_icon="fa-cubes",
)
appbuilder.add_view(
    IngredienteView,
    "Ingredientes",
    icon="fa-shopping-basket",
    category="Inventario",
)
appbuilder.add_view(
    MovimientoInventarioView,
    "Movimientos",
    icon="fa-exchange",
    category="Inventario",
)
appbuilder.add_view(
    PlatoView,
    "Platos",
    icon="fa-birthday-cake",
    category="Reposteria",
    category_icon="fa-cutlery",
)
appbuilder.add_view(
    RecetaView,
    "Recetas",
    icon="fa-book",
    category="Reposteria",
)


@app.errorhandler(404)
def page_not_found(e):
    return (
        render_template(
            "404.html", base_template=appbuilder.base_template, appbuilder=appbuilder
        ),
        404,
    )
