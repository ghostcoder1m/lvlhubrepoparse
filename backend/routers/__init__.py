from fastapi import APIRouter
from .user_item_interaction import router as user_item_interaction_router
from .workflows import router as workflows_router
from .users import router as users_router
from .leads import router as leads_router
from .campaigns import router as campaigns_router
from .offers import router as offers_router
from .messages import router as messages_router
from .funnels import router as funnels_router
from .pages import router as pages_router
from .elements import router as elements_router
from .automations import router as automations_router
from .triggers import router as triggers_router
from .actions import router as actions_router
from .aimodels import router as aimodels_router  # Importing the new aimodels router
from .ai_services import router as ai_services_router

router = APIRouter()

router.include_router(user_item_interaction_router)
router.include_router(workflows_router)
router.include_router(users_router)
router.include_router(leads_router)
router.include_router(campaigns_router)
router.include_router(offers_router)
router.include_router(messages_router)
router.include_router(funnels_router)
router.include_router(pages_router)
router.include_router(elements_router)
router.include_router(automations_router)
router.include_router(triggers_router)
router.include_router(actions_router)
router.include_router(aimodels_router)  # Including the aimodels router
router.include_router(ai_services_router)
