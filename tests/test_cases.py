from datetime import datetime

import pytest
from httpx import AsyncClient


import json

coil_create =[{"length": 5, "weight": 55}]
coil_delete_exist = [{"id": 5}]
coil_delete_not_exist = [{"id": 35}]


class TestCoil:
    @pytest.mark.parametrize("coil_create", coil_create)
    @pytest.mark.anyio
    async def test_coil_create(self, ac: AsyncClient, coil_create):
        response = await ac.post(
            "/coil",
            json=coil_create,
        )
        assert response.status_code == 200
        assert coil_create["length"] == json.loads(response.text)["length"]
        assert coil_create["weight"] == json.loads(response.text)["weight"]
        assert json.loads(response.text)["creation_date"] == datetime.date.today()

    @pytest.mark.parametrize("coil_delete_exist", coil_delete_exist)
    @pytest.mark.anyio
    async def test_delete_coil_exist(self, ac: AsyncClient, coil_delete_exist):
        response = await ac.delete(f"/coil?id={coil_delete_exist['id']}")
        assert response.status_code == 200
        assert coil_delete_exist["id"] == json.loads(response.text)["id"]
        assert json.loads(response.text)["deletion_date"] == datetime.date.today()

    @pytest.mark.parametrize("coil_delete_not_exist", coil_delete_not_exist)
    @pytest.mark.anyio
    async def test_delete_coil_not_exist(self, ac: AsyncClient, coil_delete_not_exist):
        response = await ac.delete(f"/coil?id={coil_delete_exist['id']}")
        assert response.status_code == 400





