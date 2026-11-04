
import logging
import hashlib
from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from backend.app.db.session import SessionLocal


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["Operações"])


# ============================================================
# CONEXÃO COM O BANCO DE DADOS
# ============================================================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============================================================
# CONFIGURAÇÃO DOS MÓDULOS
# ============================================================

RESOURCES = {
    "customers": {
        "table": "customers",
        "pk": "customer_id",
        "columns": [
            "full_name", "email", "phone", "is_active"
        ],
        "required": ["full_name", "email"],
        "select": """
            customer_id, full_name, email, phone,
            is_active, created_at
        """,
        "search": ["full_name", "email", "phone"],
    },

    "categories": {
        "table": "categories",
        "pk": "category_id",
        "columns": [
            "parent_category_id", "category_name", "description"
        ],
        "required": ["category_name"],
        "select": """
            category_id, parent_category_id,
            category_name, description
        """,
        "search": ["category_name", "description"],
    },

    "products": {
        "table": "products",
        "pk": "product_id",
        "columns": [
            "category_id", "sku", "product_name", "description",
            "unit_price", "unit_weight_kg",
            "is_hazardous", "is_active"
        ],
        "required": [
            "category_id", "sku", "product_name", "unit_price"
        ],
        "select": """
            p.product_id, p.category_id, c.category_name,
            p.sku, p.product_name, p.description,
            p.unit_price, p.unit_weight_kg,
            p.is_hazardous, p.is_active, p.created_at
        """,
        "from": """
            products p
            LEFT JOIN categories c
            ON c.category_id = p.category_id
        """,
        "search": [
            "p.sku", "p.product_name", "c.category_name"
        ],
    },

    "warehouses": {
        "table": "warehouses",
        "pk": "warehouse_id",
        "columns": [
            "warehouse_code", "warehouse_name", "city",
            "state_code", "country_code", "is_active"
        ],
        "required": [
            "warehouse_code", "warehouse_name", "city", "state_code"
        ],
        "select": """
            warehouse_id, warehouse_code, warehouse_name,
            city, state_code, country_code, is_active
        """,
        "search": [
            "warehouse_code", "warehouse_name", "city"
        ],
    },

    "inventory": {
        "table": "inventory",
        "pk": "inventory_id",
        "columns": [
            "product_id", "warehouse_id", "location_id",
            "quantity", "reserved_quantity"
        ],
        "required": [
            "product_id", "warehouse_id", "quantity"
        ],
        "select": """
            i.inventory_id, i.product_id, p.product_name,
            i.warehouse_id, w.warehouse_name,
            i.location_id, i.quantity,
            i.reserved_quantity, i.updated_at
        """,
        "from": """
            inventory i
            JOIN products p ON p.product_id = i.product_id
            JOIN warehouses w ON w.warehouse_id = i.warehouse_id
        """,
        "search": [
            "p.product_name", "w.warehouse_name"
        ],
    },

    "orders": {
        "table": "orders",
        "pk": "order_id",
        "columns": [
            "customer_id", "order_number", "order_status",
            "subtotal", "shipping_amount", "total_amount",
            "placed_at"
        ],
        "required": ["customer_id", "order_number"],
        "select": """
            o.order_id, o.customer_id,
            c.full_name AS customer_name,
            o.order_number, o.order_status,
            o.subtotal, o.shipping_amount,
            o.total_amount, o.placed_at, o.created_at
        """,
        "from": """
            orders o
            JOIN customers c ON c.customer_id = o.customer_id
        """,
        "search": [
            "o.order_number", "c.full_name", "o.order_status"
        ],
    },

    "deliveries": {
        "table": "deliveries",
        "pk": "delivery_id",
        "columns": [
            "order_id", "route_id", "vehicle_id", "driver_id",
            "tracking_code", "delivery_status",
            "shipped_at", "delivered_at"
        ],
        "required": ["order_id", "tracking_code"],
        "select": """
            d.delivery_id, d.order_id,
            o.order_number, d.route_id,
            d.vehicle_id, d.driver_id,
            d.tracking_code, d.delivery_status,
            d.shipped_at, d.delivered_at
        """,
        "from": """
            deliveries d
            JOIN orders o ON o.order_id = d.order_id
        """,
        "search": [
            "d.tracking_code", "o.order_number",
            "d.delivery_status"
        ],
    },

    "drivers": {
        "table": "drivers",
        "pk": "driver_id",
        "columns": ["full_name", "license_number_hash", "phone", "is_active"],
        "required": ["full_name", "license_number_hash"],
        "select": "driver_id, full_name, 'PROTEGIDO' AS license_number_hash, phone, is_active",
        "search": ["full_name", "phone"],
    },

    "vehicles": {
        "table": "vehicles",
        "pk": "vehicle_id",
        "columns": ["plate_hash", "vehicle_type", "capacity_kg", "is_active"],
        "required": ["plate_hash", "vehicle_type", "capacity_kg"],
        "select": "vehicle_id, CONCAT('VEIC-', LEFT(plate_hash, 8)) AS plate_hash, vehicle_type, capacity_kg, is_active",
        "search": ["vehicle_type"],
    },

    "routes": {
        "table": "routes",
        "pk": "route_id",
        "columns": ["route_code", "origin_warehouse_id", "destination_description", "planned_distance_km", "estimated_cost", "route_status"],
        "required": ["route_code", "origin_warehouse_id", "destination_description"],
        "select": "route_id, route_code, origin_warehouse_id, destination_description, planned_distance_km, estimated_cost, route_status, created_at",
        "search": ["route_code", "destination_description", "route_status"],
    },

    "warehouse_locations": {
        "table": "warehouse_locations",
        "pk": "location_id",
        "columns": ["warehouse_id", "aisle", "shelf", "level_no", "max_weight_kg", "hazardous_allowed", "location_status"],
        "required": ["warehouse_id", "aisle", "shelf", "level_no", "max_weight_kg"],
        "select": "location_id, warehouse_id, aisle, shelf, level_no, max_weight_kg, hazardous_allowed, location_status",
        "search": ["location_status"],
    },

    "payments": {
        "table": "payments",
        "pk": "payment_id",
        "columns": ["order_id", "payment_reference", "payment_method", "payment_status", "amount", "paid_at"],
        "required": ["order_id", "payment_method", "amount"],
        "select": "payment_id, order_id, payment_reference, payment_method, payment_status, amount, paid_at, created_at",
        "search": ["payment_reference", "payment_method", "payment_status"],
    },
}


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def get_resource(resource: str):
    cfg = RESOURCES.get(resource)

    if cfg is None:
        raise HTTPException(
            status_code=404,
            detail="Módulo não encontrado."
        )

    return cfg


def validate_payload(cfg: dict, payload: dict):
    unknown = set(payload) - set(cfg["columns"])

    if unknown:
        raise HTTPException(
            status_code=422,
            detail=f"Campos não permitidos: {', '.join(sorted(unknown))}"
        )

    missing = [
        field
        for field in cfg["required"]
        if payload.get(field) is None or payload.get(field) == ""
    ]

    if missing:
        raise HTTPException(
            status_code=422,
            detail=f"Campos obrigatórios: {', '.join(missing)}"
        )


def decimal_value(value: Any, field: str) -> Decimal:
    try:
        return Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        raise HTTPException(
            status_code=422,
            detail=f"Valor inválido para o campo {field}."
        )


def prepare_payload(resource: str, payload: dict):
    data = dict(payload)

    if resource == "customers":
        data.setdefault("is_active", True)

    elif resource == "products":
        price = decimal_value(data["unit_price"], "unit_price")

        if price < 0:
            raise HTTPException(
                status_code=422,
                detail="O preço não pode ser negativo."
            )

        data["unit_price"] = price
        data.setdefault("unit_weight_kg", 0)
        data.setdefault("is_hazardous", False)
        data.setdefault("is_active", True)

    elif resource == "warehouses":
        data.setdefault("country_code", "BR")
        data.setdefault("is_active", True)

        for field in ("warehouse_code", "warehouse_name", "city"):
            if isinstance(data.get(field), str):
                data[field] = data[field].strip()

        if isinstance(data.get("state_code"), str):
            data["state_code"] = data["state_code"].strip().upper()

        if isinstance(data.get("country_code"), str):
            data["country_code"] = data["country_code"].strip().upper()

        if len(data["state_code"]) != 2:
            raise HTTPException(
                status_code=422,
                detail="A UF deve conter exatamente duas letras."
            )

        if len(data["country_code"]) != 2:
            raise HTTPException(
                status_code=422,
                detail="O código do país deve conter duas letras."
            )

    elif resource == "inventory":
        quantity = decimal_value(data["quantity"], "quantity")
        reserved = decimal_value(
            data.get("reserved_quantity", 0),
            "reserved_quantity"
        )

        if quantity < 0 or reserved < 0 or reserved > quantity:
            raise HTTPException(
                status_code=422,
                detail="A quantidade reservada deve estar entre zero e a quantidade total."
            )

        data.setdefault("reserved_quantity", 0)

    elif resource == "orders":
        data.setdefault("order_status", "DRAFT")
        data.setdefault("subtotal", 0)
        data.setdefault("shipping_amount", 0)

        subtotal = decimal_value(data["subtotal"], "subtotal")
        shipping = decimal_value(
            data["shipping_amount"], "shipping_amount"
        )

        if subtotal < 0 or shipping < 0:
            raise HTTPException(
                status_code=422,
                detail="Os valores do pedido não podem ser negativos."
            )

        data.setdefault("total_amount", subtotal + shipping)

    elif resource == "deliveries":
        data.setdefault("delivery_status", "PENDING")

    elif resource == "drivers":
        raw_license = str(data["license_number_hash"]).strip()
        data["license_number_hash"] = hashlib.sha256(raw_license.encode("utf-8")).hexdigest()
        data.setdefault("is_active", True)

    elif resource == "vehicles":
        raw_plate = str(data["plate_hash"]).strip().upper()
        if not raw_plate:
            raise HTTPException(status_code=422, detail="Informe a identificação da placa.")
        data["plate_hash"] = hashlib.sha256(raw_plate.encode("utf-8")).hexdigest()
        data["capacity_kg"] = decimal_value(data["capacity_kg"], "capacity_kg")
        if data["capacity_kg"] <= 0:
            raise HTTPException(status_code=422, detail="A capacidade deve ser maior que zero.")
        data.setdefault("is_active", True)

    elif resource == "routes":
        data.setdefault("planned_distance_km", 0)
        data.setdefault("estimated_cost", 0)
        data.setdefault("route_status", "PLANNED")
        data["planned_distance_km"] = decimal_value(data["planned_distance_km"], "planned_distance_km")
        data["estimated_cost"] = decimal_value(data["estimated_cost"], "estimated_cost")
        if data["planned_distance_km"] < 0 or data["estimated_cost"] < 0:
            raise HTTPException(status_code=422, detail="Distância e custo não podem ser negativos.")

    elif resource == "warehouse_locations":
        data.setdefault("hazardous_allowed", False)
        data.setdefault("location_status", "AVAILABLE")
        data["max_weight_kg"] = decimal_value(data["max_weight_kg"], "max_weight_kg")
        if data["max_weight_kg"] <= 0:
            raise HTTPException(status_code=422, detail="A capacidade máxima deve ser maior que zero.")

    elif resource == "payments":
        data.setdefault("payment_status", "PENDING")
        if "amount" in data:
            data["amount"] = decimal_value(data["amount"], "amount")
            if data["amount"] <= 0:
                raise HTTPException(status_code=422, detail="O valor do pagamento deve ser maior que zero.")
        allowed_methods = {"PIX", "CREDIT_CARD", "DEBIT_CARD", "BOLETO", "CASH", "OTHER"}
        allowed_statuses = {"PENDING", "AUTHORIZED", "PAID", "REFUNDED", "FAILED"}
        if "payment_method" in data and data["payment_method"] not in allowed_methods:
            raise HTTPException(status_code=422, detail="Forma de pagamento inválida.")
        if "payment_status" in data and data["payment_status"] not in allowed_statuses:
            raise HTTPException(status_code=422, detail="Status de pagamento inválido.")
        if data.get("payment_status") == "PAID":
            data.setdefault("paid_at", datetime.now())

    return data


# ============================================================
# PAINEL PRINCIPAL
# ============================================================

@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db)):
    try:
        result = {}

        tables = [
            ("customers", "customers"),
            ("products", "products"),
            ("orders", "orders"),
            ("inventory", "inventory"),
            ("deliveries", "deliveries"),
            ("warehouses", "warehouses"),
            ("drivers", "drivers"),
            ("vehicles", "vehicles"),
            ("routes", "routes"),
            ("payments", "payments"),
        ]

        for table, key in tables:
            result[key] = db.execute(
                text(f"SELECT COUNT(*) FROM {table}")
            ).scalar_one()

        result["order_revenue"] = db.execute(
            text("""
                SELECT COALESCE(SUM(total_amount), 0)
                FROM orders
                WHERE order_status <> 'CANCELLED'
            """)
        ).scalar_one()

        result["pending_deliveries"] = db.execute(
            text("""
                SELECT COUNT(*)
                FROM deliveries
                WHERE delivery_status NOT IN ('DELIVERED', 'EXCEPTION')
            """)
        ).scalar_one()

        return jsonable_encoder(result)

    except SQLAlchemyError:
        logger.exception("Erro ao carregar o painel.")
        raise HTTPException(
            status_code=503,
            detail="Não foi possível carregar os indicadores."
        )


# ============================================================
# LISTAR REGISTROS
# ============================================================

@router.get("/{resource}")
def list_resource(
    resource: str,
    q: str | None = None,
    limit: int = 200,
    db: Session = Depends(get_db)
):
    cfg = get_resource(resource)

    limit = max(1, min(limit, 500))

    source = cfg.get("from", cfg["table"])

    query = f"SELECT {cfg['select']} FROM {source}"

    params = {"limit": limit}

    if q:
        clauses = [
            f"{column} LIKE :term"
            for column in cfg.get("search", [])
        ]

        if clauses:
            query += " WHERE (" + " OR ".join(clauses) + ")"
            params["term"] = f"%{q}%"

    query += f" ORDER BY {cfg['pk']} DESC LIMIT :limit"

    try:
        rows = db.execute(
            text(query), params
        ).mappings().all()

        return jsonable_encoder([dict(row) for row in rows])

    except SQLAlchemyError:
        logger.exception("Erro ao listar o módulo %s.", resource)
        raise HTTPException(
            status_code=503,
            detail="Erro ao consultar os registros."
        )


# ============================================================
# CADASTRAR REGISTROS
# ============================================================

@router.post(
    "/{resource}",
    status_code=status.HTTP_201_CREATED
)
def create_resource(
    resource: str,
    payload: dict[str, Any],
    db: Session = Depends(get_db)
):
    cfg = get_resource(resource)

    validate_payload(cfg, payload)

    data = prepare_payload(resource, payload)

    keys = list(data.keys())

    columns = ", ".join(keys)
    binds = ", ".join(f":{key}" for key in keys)

    query = text(
        f"INSERT INTO {cfg['table']} ({columns}) "
        f"VALUES ({binds})"
    )

    try:
        result = db.execute(query, data)

        if resource == "payments" and data.get("payment_status") == "PAID":
            db.execute(
                text("UPDATE orders SET order_status = 'PAID' WHERE order_id = :order_id"),
                {"order_id": data["order_id"]},
            )

        db.commit()

        return {
            "id": result.lastrowid,
            "message": "Registro criado com sucesso."
        }

    except HTTPException:
        db.rollback()
        raise

    except IntegrityError as exc:
        db.rollback()
        logger.exception(
            "Conflito de integridade ao cadastrar %s.", resource
        )

        raise HTTPException(
            status_code=409,
            detail="Conflito: verifique códigos duplicados e vínculos existentes."
        ) from exc

    except SQLAlchemyError as exc:
        db.rollback()
        logger.exception(
            "Erro SQL ao cadastrar %s.", resource
        )

        raise HTTPException(
            status_code=400,
            detail="Não foi possível gravar os dados no banco."
        ) from exc


# ============================================================
# ATUALIZAR REGISTROS
# ============================================================

@router.put("/{resource}/{record_id}")
def update_resource(
    resource: str,
    record_id: int,
    payload: dict[str, Any],
    db: Session = Depends(get_db)
):
    cfg = get_resource(resource)

    if not payload:
        raise HTTPException(
            status_code=422,
            detail="Informe os campos que deseja atualizar."
        )

    validate_payload(
        {
            **cfg,
            "required": []
        },
        payload
    )

    data = prepare_payload(resource, payload)

    assignments = ", ".join(
        f"{key} = :{key}"
        for key in data
    )

    params = dict(data)
    params["record_id"] = record_id

    query = text(
        f"UPDATE {cfg['table']} "
        f"SET {assignments} "
        f"WHERE {cfg['pk']} = :record_id"
    )

    try:
        result = db.execute(query, params)

        if result.rowcount == 0:
            db.rollback()
            raise HTTPException(
                status_code=404,
                detail="Registro não encontrado."
            )

        if resource == "payments" and data.get("payment_status") == "PAID":
            db.execute(
                text("""
                    UPDATE orders
                    SET order_status = 'PAID'
                    WHERE order_id = (
                        SELECT order_id FROM payments WHERE payment_id = :record_id
                    )
                """),
                {"record_id": record_id},
            )

        db.commit()

        return {
            "message": "Registro atualizado com sucesso."
        }

    except HTTPException:
        raise

    except IntegrityError as exc:
        db.rollback()
        logger.exception("Conflito ao atualizar %s.", resource)

        raise HTTPException(
            status_code=409,
            detail="Atualização não permitida devido a duplicidade ou vínculo."
        ) from exc

    except SQLAlchemyError as exc:
        db.rollback()
        logger.exception("Erro ao atualizar %s.", resource)

        raise HTTPException(
            status_code=400,
            detail="Não foi possível atualizar o registro."
        ) from exc


# ============================================================
# EXCLUIR REGISTROS
# ============================================================

@router.delete("/{resource}/{record_id}")
def delete_resource(
    resource: str,
    record_id: int,
    db: Session = Depends(get_db)
):
    cfg = get_resource(resource)

    query = text(
        f"DELETE FROM {cfg['table']} "
        f"WHERE {cfg['pk']} = :record_id"
    )

    try:
        result = db.execute(
            query,
            {"record_id": record_id}
        )

        if result.rowcount == 0:
            db.rollback()
            raise HTTPException(
                status_code=404,
                detail="Registro não encontrado."
            )

        db.commit()

        return {
            "message": "Registro excluído com sucesso."
        }

    except HTTPException:
        raise

    except IntegrityError as exc:
        db.rollback()
        logger.exception("Conflito ao excluir %s.", resource)

        raise HTTPException(
            status_code=409,
            detail="O registro possui vínculos e não pode ser excluído."
        ) from exc

    except SQLAlchemyError as exc:
        db.rollback()
        logger.exception("Erro ao excluir %s.", resource)

        raise HTTPException(
            status_code=400,
            detail="Não foi possível excluir o registro."
        ) from exc
