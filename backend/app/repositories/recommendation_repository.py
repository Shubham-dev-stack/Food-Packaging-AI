"""Repository for persisting and querying recommendation audit sessions."""

from sqlalchemy.orm import Session, joinedload

from backend.app.models.recommendation import RecommendationRequest, RecommendationResult


class RecommendationRepository:
    """Persistence abstraction for recommendation requests and results."""

    @staticmethod
    def create_request(db: Session, request: RecommendationRequest) -> RecommendationRequest:
        """Persist a recommendation request audit record."""
        db.add(request)
        db.commit()
        db.refresh(request)
        return request

    @staticmethod
    def create_result(db: Session, result: RecommendationResult) -> RecommendationResult:
        """Persist a recommendation result audit record."""
        db.add(result)
        db.commit()
        db.refresh(result)
        return result

    @staticmethod
    def get_request_by_id(db: Session, request_id: str) -> RecommendationRequest | None:
        """Retrieve a recommendation request by ID with linked commodity and result."""
        return (
            db.query(RecommendationRequest)
            .options(
                joinedload(RecommendationRequest.commodity),
                joinedload(RecommendationRequest.result),
            )
            .filter(RecommendationRequest.request_id == request_id)
            .first()
        )

    @staticmethod
    def get_result_by_request_id(db: Session, request_id: str) -> RecommendationResult | None:
        """Retrieve a recommendation result by its request session ID."""
        return (
            db.query(RecommendationResult)
            .options(
                joinedload(RecommendationResult.request),
                joinedload(RecommendationResult.primary_material),
                joinedload(RecommendationResult.alternative_material),
            )
            .filter(RecommendationResult.request_id == request_id)
            .first()
        )
