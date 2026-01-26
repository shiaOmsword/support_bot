from dataclasses import dataclass
from aiogram.fsm.context import FSMContext

@dataclass(frozen=True)
class NavState:
    stack: list[str]

    @property
    def current(self) -> str:
        return self.stack[-1] if self.stack else "roles"

    def push(self, screen: str) -> "NavState":
        if self.stack and self.stack[-1] == screen:
            return self
        return NavState(stack=[*self.stack, screen])

    def back(self) -> "NavState":
        if len(self.stack) <= 1:
            return NavState(stack=["roles"])
        return NavState(stack=self.stack[:-1])

async def get_nav(state: FSMContext) -> NavState:
    data = await state.get_data()
    return NavState(stack=list(data.get("nav_stack") or ["roles"]))

async def set_nav(state: FSMContext, nav: NavState) -> None:
    await state.update_data(nav_stack=nav.stack)
