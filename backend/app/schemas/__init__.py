from backend.app.schemas.auth import Token, TokenPayload, LoginRequest, RegisterRequest
from backend.app.schemas.user import UserResponse, UserProfileResponse, UserProfileUpdate
from backend.app.schemas.assessment import (
    AssessmentQuestionResponse,
    SubmitAssessmentRequest,
    AssessmentResultResponse,
    SkillMetricResponse,
    UpdateConfidenceRequest
)
from backend.app.schemas.practice import (
    CodingProblemSummary,
    CodingProblemDetail,
    CodingRunRequest,
    CodingSubmitRequest,
    CodingExecutionResponse,
    SqlProblemSummary,
    SqlProblemDetail,
    SqlExecuteRequest,
    SqlExecutionResponse
)
from backend.app.schemas.interview import (
    StartInterviewRequest,
    AnswerInterviewQuestionRequest,
    InterviewExchangeResponse,
    InterviewSessionDetailResponse
)
from backend.app.schemas.study_plan import (
    StudyTaskCreate,
    StudyTaskUpdate,
    StudyTaskResponse,
    RecordSessionRequest,
    GeneratePlanRequest,
    StudyPlanResponse
)
from backend.app.schemas.job_tracker import (
    JobApplicationCreate,
    JobApplicationUpdate,
    JobApplicationResponse,
    JobPipelineStats
)
from backend.app.schemas.weekly import WeeklyReportResponse, GenerateWeeklyReportRequest
from backend.app.schemas.ai import (
    CoachChatRequest,
    CoachChatResponse,
    ResumeAnalyzeRequest,
    ResumeAnalyzeResponse,
    ProjectInterviewPrepRequest,
    ProjectInterviewPrepResponse
)

__all__ = [
    "Token", "TokenPayload", "LoginRequest", "RegisterRequest",
    "UserResponse", "UserProfileResponse", "UserProfileUpdate",
    "AssessmentQuestionResponse", "SubmitAssessmentRequest", "AssessmentResultResponse", "SkillMetricResponse", "UpdateConfidenceRequest",
    "CodingProblemSummary", "CodingProblemDetail", "CodingRunRequest", "CodingSubmitRequest", "CodingExecutionResponse",
    "SqlProblemSummary", "SqlProblemDetail", "SqlExecuteRequest", "SqlExecutionResponse",
    "StartInterviewRequest", "AnswerInterviewQuestionRequest", "InterviewExchangeResponse", "InterviewSessionDetailResponse",
    "StudyTaskCreate", "StudyTaskUpdate", "StudyTaskResponse", "RecordSessionRequest", "GeneratePlanRequest", "StudyPlanResponse",
    "JobApplicationCreate", "JobApplicationUpdate", "JobApplicationResponse", "JobPipelineStats",
    "WeeklyReportResponse", "GenerateWeeklyReportRequest",
    "CoachChatRequest", "CoachChatResponse", "ResumeAnalyzeRequest", "ResumeAnalyzeResponse", "ProjectInterviewPrepRequest", "ProjectInterviewPrepResponse"
]
