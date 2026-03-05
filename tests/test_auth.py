import pytest
import allure


@allure.feature("身份认证模块")
class TestAuth:

    @allure.story("用户注册与登录闭环测试")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.asyncio
    async def test_register_and_login(self, client):
        with allure.step("第一步：准备注册数据并提交"):
            user_data = {"username": "testuser", "password": "testpassword"}
            register_res = await client.post("/api/v1/users/register", json=user_data)
            assert register_res.status_code == 200

        with allure.step("第二步：使用注册账号进行登录"):
            login_data = {"username": "testuser", "password": "testpassword"}
            login_res = await client.post("/api/v1/users/login", data=login_data)
            assert login_res.status_code == 200

        with allure.step("第三步：验证返回的 Token 格式"):
            token_data = login_res.json()
            assert "access_token" in token_data
            assert token_data["token_type"] == "bearer"

    @allure.story("受保护接口访问测试")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.asyncio
    async def test_create_todo_with_token(self, client):
        with allure.step("准备工作：获取有效的访问令牌"):
            login_data = {"username": "testuser", "password": "testpassword"}
            login_res = await client.post("/api/v1/users/login", data=login_data)
            token = login_res.json()["access_token"]
            headers = {"Authorization": f"Bearer {token}"}

        with allure.step("执行操作：携带 Token 创建待办事项"):
            todo_data = {"title": "准备技术面试", "priority": 1}
            # 注意：这里我们使用了之前定义的 /todos/ 路由
            create_res = await client.post("/api/v1/todos/", json=todo_data, headers=headers)

        with allure.step("结果验证：检查状态码与数据一致性"):
            assert create_res.status_code == 200
            assert create_res.json()["title"] == "准备技术面试"