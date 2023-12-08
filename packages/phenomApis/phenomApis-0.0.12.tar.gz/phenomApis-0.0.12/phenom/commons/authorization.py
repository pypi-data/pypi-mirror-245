from phenom.commons.get_token import tokengeneration
from phenom.api.resumeparser.resume_parsing_api import ResumeParsingApi
from phenom.api.exsearch.employees_api import EmployeesApi
from phenom.api.exsearch.mentor_api import MentorApi
from phenom.api.prediction.prediction_api import PredictionApi
from phenom.api.aisourcing.ai_matching_api import AIMatchingApi
from phenom.api.search.jobs_api import JobsApi
from phenom.api.jobparser.job_parsing_api import JobParsingApi
from phenom.api.recomendation.recommendations_api import RecommendationsApi

from phenom.api.applicants.applicants_api import ApplicantsApi
from phenom.api.applicants.leads_api import LeadsApi
from phenom.api.applicants.activity_api import ActivityApi
from phenom.api.applicants.hiring_status_api import HiringStatusApi
from phenom.api.jobactivities.job_category_api import JobCategoryApi
from phenom.api.jobactivities.job_attachments_api import JobAttachmentsApi
from phenom.api.jobactivities.job_notes_api import JobNotesApi
from phenom.api.jobactivities.hiring_team_api import HiringTeamApi
from phenom.api.jobquestionarie.job_questionnaire_api import JobQuestionnaireApi
from phenom.api.jobquestionarie.questionnaire_templates_api import QuestionnaireTemplatesApi
from phenom.api.notes.notes_api import NotesApi
from phenom.api.projects.candidates_api import CandidatesApi as projectsCandidatesApi
from phenom.api.projects.workflows_api import WorkflowsApi
from phenom.api.projects.projects_api import ProjectsApi
from phenom.api.projects.workflow_status_api import WorkflowStatusApi
from phenom.api.tags.tags_api import TagsApi
from phenom.api.tags.candidates_api import CandidatesApi as tagsCandidatesApi
from phenom.api.candidates.candidates_api import CandidatesApi
from phenom.api.candidates.notes_api import NotesApi as candidatesNotes


class Authorization(object):
    def __init__(self, url, client_id, client_secret, gateway_url, apikey=None):
        self.url = url
        self.client_id = client_id
        self.client_secret = client_secret
        self.gateway_url = gateway_url
        self.apikey = apikey

    def token(self):
        return tokengeneration(self.url, self.client_id, self.client_secret)

    # resumeparser api methods
    def resume_parsing(self):
        return ResumeParsingApi(self.token(), self.gateway_url, self.apikey)

    # employee search api methods
    def employees(self):
        return EmployeesApi(self.token(), self.gateway_url, self.apikey)

    def mentors(self):
        return MentorApi(self.token(), self.gateway_url, self.apikey)

    # prediction api methods
    def prediction(self):
        return PredictionApi(self.token(), self.gateway_url, self.apikey)

    # ai-sourcing api methods
    def ai_sourcing(self):
        return AIMatchingApi(self.token(), self.gateway_url, self.apikey)

    # search api methods
    def search(self):
        return JobsApi(self.token(), self.gateway_url, self.apikey)

    # job-parser api methods
    def job_parser(self):
        return JobParsingApi(self.token(), self.gateway_url, self.apikey)

    # recommendation api methods
    def recommendation(self):
        return RecommendationsApi(self.token(), self.gateway_url, self.apikey)

    # applicants api methods
    def applicants(self):
        return ApplicantsApi(self.token(), self.gateway_url, self.apikey)

    def activity(self):
        return ActivityApi(self.token(), self.gateway_url, self.apikey)

    def hiring_status(self):
        return HiringStatusApi(self.token(), self.gateway_url, self.apikey)

    def leads(self):
        return LeadsApi(self.token(), self.gateway_url, self.apikey)

    # job activities api methods
    def hiring_team(self):
        return HiringTeamApi(self.token(), self.gateway_url, self.apikey)

    def job_attachments(self):
        return JobAttachmentsApi(self.token(), self.gateway_url, self.apikey)

    def job_category(self):
        return JobCategoryApi(self.token(), self.gateway_url, self.apikey)

    def job_notes(self):
        return JobNotesApi(self.token(), self.gateway_url, self.apikey)

    # job questionaire api methods
    def job_questionaire(self):
        return JobQuestionnaireApi(self.token(), self.gateway_url, self.apikey)

    def questionaire_templates(self):
        return QuestionnaireTemplatesApi(self.token(), self.gateway_url, self.apikey)

    # notes api method
    def notes(self):
        return NotesApi(self.token(), self.gateway_url, self.apikey)

    # projects api methods
    def projects_candidates(self):
        return projectsCandidatesApi(self.token(), self.gateway_url, self.apikey)

    def projects(self):
        return ProjectsApi(self.token(), self.gateway_url, self.apikey)

    def workflow_status(self):
        return WorkflowStatusApi(self.token(), self.gateway_url, self.apikey)

    def workflows(self):
        return WorkflowsApi(self.token(), self.gateway_url, self.apikey)

    # tags api methods
    def tags_candidates(self):
        return tagsCandidatesApi(self.token(), self.gateway_url, self.apikey)

    def tags(self):
        return TagsApi(self.token(), self.gateway_url, self.apikey)

    # candidates api methods
    def candidates(self):
        return CandidatesApi(self.token(), self.gateway_url, self.apikey)

    def candidates_notes(self):
        return candidatesNotes(self.token(), self.gateway_url, self.apikey)
