"""Benchmark latency tung buoc cua pipeline SafeRAG.

Do thoi gian trung binh (ms) cua tung component:
- Safety router
- Ambiguity checker
- Hybrid retrieval (BM25 + Chroma)
- Evidence guardrail
- LLM response (neu co key)
- Tong end-to-end

Ket qua xuat ra JSON va in bang so sanh.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import sys
import time
from pathlib import Path
from statistics import mean, median, stdev
from typing import Any, Dict, List

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


# Cau hoi dai dien cho cac loai intent khac nhau
CAU_HOI_BENCHMARK: List[Dict[str, Any]] = [
    {"id": "latency_01", "nhom": "tra_cuu_thuoc",    "cau_hoi": "Paracetamol dung de lam gi?"},
    {"id": "latency_02", "nhom": "tra_cuu_thuoc",    "cau_hoi": "Ibuprofen co tac dung gi?"},
    {"id": "latency_03", "nhom": "lieu_dung",         "cau_hoi": "Paracetamol nguoi lon uong lieu bao nhieu?"},
    {"id": "latency_04", "nhom": "tuong_tac",         "cau_hoi": "Warfarin va Aspirin uong cung duoc khong?"},
    {"id": "latency_05", "nhom": "tuong_tac",         "cau_hoi": "Clarithromycin va Atorvastatin co tuong tac khong?"},
    {"id": "latency_06", "nhom": "benh_nen",          "cau_hoi": "Nguoi suy than uong Ibuprofen co an toan khong?"},
    {"id": "latency_07", "nhom": "benh_nen",          "cau_hoi": "Cao huyet ap uong Pseudoephedrine co duoc khong?"},
    {"id": "latency_08", "nhom": "cap_cuu",           "cau_hoi": "Dau nguc du doi phai lam gi?"},
    {"id": "latency_09", "nhom": "cap_cuu",           "cau_hoi": "Uong nham 20 vien paracetamol phai lam the nao?"},
    {"id": "latency_10", "nhom": "tu_van_otc",        "cau_hoi": "Bi cam cum uong thuoc gi?"},
    {"id": "latency_11", "nhom": "tu_van_otc",        "cau_hoi": "Dau dau nen mua thuoc gi khong can don?"},
    {"id": "latency_12", "nhom": "nhi_khoa",          "cau_hoi": "Con toi 3 tuoi bi sot uong thuoc gi?"},
    {"id": "latency_13", "nhom": "nhi_khoa",          "cau_hoi": "Tre so sinh dung thuoc nhu the nao?"},
    {"id": "latency_14", "nhom": "mang_thai",         "cau_hoi": "Mang thai 3 thang dau dau uong gi?"},
    {"id": "latency_15", "nhom": "sai_chinh_ta",      "cau_hoi": "Tetracylin lieu dung nhu the nao?"},
]


def cau_hinh_stdout() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")


async def do_mot_cau(dich_vu: Any, cau: Dict[str, Any]) -> Dict[str, Any]:
    """Do thoi gian end-to-end cho mot cau hoi va lay trace cac buoc."""
    thoi_diem_bat_dau = time.perf_counter()
    phan_hoi = await dich_vu.answer(cau["cau_hoi"], session_id=f"bench-{cau['id']}")
    thoi_gian_tong = (time.perf_counter() - thoi_diem_bat_dau) * 1000  # ms

    metadata = phan_hoi.metadata or {}
    agent_pipeline = metadata.get("agent_pipeline") or {}
    trace = agent_pipeline.get("trace") or []

    # Trich xuat thoi gian tung buoc tu trace neu co
    thoi_gian_buoc: Dict[str, float] = {}
    for buoc in trace:
        ten_node = buoc.get("node", "")
        thoi_gian_ms = buoc.get("duration_ms") or buoc.get("elapsed_ms") or 0.0
        if ten_node and thoi_gian_ms:
            thoi_gian_buoc[ten_node] = round(float(thoi_gian_ms), 2)

    return {
        "id": cau["id"],
        "nhom": cau["nhom"],
        "cau_hoi": cau["cau_hoi"],
        "hanh_dong": metadata.get("rag_action"),
        "y_dinh": metadata.get("intent"),
        "thoi_gian_tong_ms": round(thoi_gian_tong, 2),
        "thoi_gian_buoc": thoi_gian_buoc,
        "so_nguon": len(phan_hoi.sources or []),
        "co_canh_bao": bool(phan_hoi.warnings),
    }


def tong_hop_latency(ket_qua: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Tinh toan cac chi so thong ke latency tong the va theo nhom."""
    tat_ca_ms = [r["thoi_gian_tong_ms"] for r in ket_qua]

    # Thong ke theo nhom
    theo_nhom: Dict[str, List[float]] = {}
    for r in ket_qua:
        theo_nhom.setdefault(r["nhom"], []).append(r["thoi_gian_tong_ms"])

    thong_ke_nhom = {}
    for nhom, ds_ms in theo_nhom.items():
        thong_ke_nhom[nhom] = {
            "so_luong": len(ds_ms),
            "trung_binh_ms": round(mean(ds_ms), 1),
            "trung_vi_ms": round(median(ds_ms), 1),
            "nhanh_nhat_ms": round(min(ds_ms), 1),
            "cham_nhat_ms": round(max(ds_ms), 1),
        }

    # Thong ke buoc chi tiet (neu trace co data)
    tat_ca_buoc: Dict[str, List[float]] = {}
    for r in ket_qua:
        for ten_buoc, ms in r["thoi_gian_buoc"].items():
            tat_ca_buoc.setdefault(ten_buoc, []).append(ms)
    thong_ke_buoc = {
        ten: round(mean(ds), 1)
        for ten, ds in tat_ca_buoc.items()
    }

    return {
        "tong_cau_hoi": len(ket_qua),
        "trung_binh_ms": round(mean(tat_ca_ms), 1),
        "trung_vi_ms": round(median(tat_ca_ms), 1),
        "do_lech_chuan_ms": round(stdev(tat_ca_ms), 1) if len(tat_ca_ms) > 1 else 0.0,
        "p95_ms": round(sorted(tat_ca_ms)[int(len(tat_ca_ms) * 0.95)], 1) if len(tat_ca_ms) >= 2 else tat_ca_ms[0],
        "nhanh_nhat_ms": round(min(tat_ca_ms), 1),
        "cham_nhat_ms": round(max(tat_ca_ms), 1),
        "theo_nhom": thong_ke_nhom,
        "trung_binh_buoc_ms": thong_ke_buoc,
    }


def in_bang_ket_qua(ket_qua: List[Dict[str, Any]], tong_hop: Dict[str, Any]) -> None:
    """In bang ket qua ra stdout."""
    print("\n" + "=" * 70)
    print("  LATENCY BENCHMARK — SAFERAG PHARMA PIPELINE")
    print("=" * 70)
    print(f"{'ID':<14} {'Nhom':<18} {'Hanh dong':<22} {'Thoi gian (ms)':>14}")
    print("-" * 70)
    for r in ket_qua:
        print(
            f"{r['id']:<14} {r['nhom']:<18} {(r['hanh_dong'] or 'n/a'):<22} "
            f"{r['thoi_gian_tong_ms']:>14.1f}"
        )
    print("=" * 70)
    print(f"  Trung binh : {tong_hop['trung_binh_ms']:>8.1f} ms")
    print(f"  Trung vi   : {tong_hop['trung_vi_ms']:>8.1f} ms")
    print(f"  Do lech chuan : {tong_hop['do_lech_chuan_ms']:>5.1f} ms")
    print(f"  P95        : {tong_hop['p95_ms']:>8.1f} ms")
    print(f"  Nhanh nhat : {tong_hop['nhanh_nhat_ms']:>8.1f} ms")
    print(f"  Cham nhat  : {tong_hop['cham_nhat_ms']:>8.1f} ms")
    print("=" * 70)

    if tong_hop["theo_nhom"]:
        print("\nThong ke theo nhom:")
        print(f"  {'Nhom':<22} {'So luong':>8} {'TB (ms)':>10} {'Min':>8} {'Max':>8}")
        print("  " + "-" * 60)
        for nhom, s in sorted(tong_hop["theo_nhom"].items()):
            print(
                f"  {nhom:<22} {s['so_luong']:>8} {s['trung_binh_ms']:>10.1f} "
                f"{s['nhanh_nhat_ms']:>8.1f} {s['cham_nhat_ms']:>8.1f}"
            )

    if tong_hop["trung_binh_buoc_ms"]:
        print("\nTrung binh thoi gian tung buoc pipeline:")
        for ten_buoc, ms in sorted(tong_hop["trung_binh_buoc_ms"].items(), key=lambda x: -x[1]):
            print(f"  {ten_buoc:<40} {ms:>8.1f} ms")
    print()


async def chay_benchmark(dung_chroma: bool, thu_muc_xuat: str, so_vong_lap: int) -> None:
    cau_hinh_stdout()
    from backend.services.safe_rag_service import SafeRagService

    kwargs = {}
    if not dung_chroma:
        kwargs["chroma_dir"] = Path("__missing_chroma_for_bench__")
    dich_vu = SafeRagService(**kwargs)

    tat_ca_ket_qua: List[Dict[str, Any]] = []
    print(f"\nBat dau benchmark: {len(CAU_HOI_BENCHMARK)} cau x {so_vong_lap} vong lap ...")

    for vong in range(so_vong_lap):
        for cau in CAU_HOI_BENCHMARK:
            print(f"  [{vong+1}/{so_vong_lap}] {cau['id']} — {cau['cau_hoi'][:55]}...")
            r = await do_mot_cau(dich_vu, cau)
            r["vong_lap"] = vong + 1
            tat_ca_ket_qua.append(r)

    # Tinh toan thong ke
    tong_hop = tong_hop_latency(tat_ca_ket_qua)

    # In ket qua
    in_bang_ket_qua(tat_ca_ket_qua, tong_hop)

    # Luu file JSON
    thu_muc = Path(thu_muc_xuat)
    thu_muc.mkdir(parents=True, exist_ok=True)
    duong_dan_chi_tiet = thu_muc / "latency_benchmark_details.json"
    duong_dan_tong_hop = thu_muc / "latency_benchmark_summary.json"
    duong_dan_chi_tiet.write_text(
        json.dumps(tat_ca_ket_qua, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    duong_dan_tong_hop.write_text(
        json.dumps(tong_hop, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"Da luu ket qua vao:\n  {duong_dan_chi_tiet}\n  {duong_dan_tong_hop}")


def main() -> None:
    bo_phan_tich = argparse.ArgumentParser(description="Benchmark latency pipeline SafeRAG")
    bo_phan_tich.add_argument("--dung-chroma", action="store_true", help="Ket noi Chroma that (yeu cau index)")
    bo_phan_tich.add_argument("--thu-muc-xuat", default="data/evaluation", help="Thu muc luu ket qua")
    bo_phan_tich.add_argument("--vong-lap", type=int, default=1, help="So vong lap de tinh trung binh (mac dinh: 1)")
    tham_so = bo_phan_tich.parse_args()
    asyncio.run(chay_benchmark(tham_so.dung_chroma, tham_so.thu_muc_xuat, tham_so.vong_lap))


if __name__ == "__main__":
    main()
