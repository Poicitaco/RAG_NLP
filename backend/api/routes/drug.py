"""
Các endpoint API quản lý thông tin thuốc.
"""
from fastapi import APIRouter, HTTPException
from backend.models import (
    DrugQuery,
    DrugInteractionCheck,
    DosageRequest,
)
from backend.services.drug_registry_service import get_drug_registry_service
from backend.utils import app_logger, format_response

router = APIRouter()


@router.post("/search")
async def search_drugs(query: DrugQuery):
    """Tìm kiếm thuốc theo tên hoặc danh mục"""
    try:
        service = get_drug_registry_service()
        drugs = service.search(query.query, limit=query.limit)
        return format_response(
            success=True,
            data={
                "drugs": drugs,
                "total": len(drugs),
                "query": query.query
            },
            message="Tìm kiếm thuốc hoàn tất",
            metadata={"source": "dav_registry_jsonl"},
        )
    except Exception as e:
        app_logger.error(f"Lỗi khi tìm kiếm thuốc: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/check-interaction")
async def check_drug_interactions(request: DrugInteractionCheck):
    """Kiểm tra tương tác giữa nhiều thuốc"""
    try:
        service = get_drug_registry_service()
        result = service.check_interactions(request.drugs)
        return format_response(
            success=True,
            data=result,
            message="Kiểm tra tương tác hoàn tất",
            metadata={"source": "ddinter_graph_safety"},
        )
    except Exception as e:
        app_logger.error(f"Lỗi khi kiểm tra tương tác: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/dosage-advice")
async def get_dosage_advice(request: DosageRequest):
    """Lấy gợi ý liều lượng"""
    try:
        service = get_drug_registry_service()
        result = service.dosage_lookup(request.drug_name)
        if request.age is not None:
            result["patient_age"] = request.age
        if request.weight is not None:
            result["patient_weight"] = request.weight
        if request.prescription_text:
            result["prescription_text_provided"] = True
        return format_response(
            success=True,
            data=result,
            message="Đã cung cấp thông tin đối chiếu liều an toàn",
            metadata={
                "mode": "safety_lookup_only",
                "dosage_generated": False,
                "requires_clinician_or_pharmacist": True,
            },
        )
    except Exception as e:
        app_logger.error(f"Lỗi khi lấy tư vấn liều lượng: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{drug_id}")
async def get_drug_details(drug_id: str):
    """Lấy thông tin chi tiết về một thuốc cụ thể"""
    try:
        service = get_drug_registry_service()
        drug = service.get(drug_id)
        if drug:
            return format_response(
                success=True,
                data=drug,
                message="Lấy thông tin thuốc thành công",
                metadata={"source": "dav_registry_jsonl"},
            )
        return format_response(
            success=False,
            data=None,
            message=f"Không tìm thấy thuốc {drug_id}"
        )
    except Exception as e:
        app_logger.error(f"Lỗi khi lấy thông tin thuốc: {e}")
        raise HTTPException(status_code=500, detail=str(e))
