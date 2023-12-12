from jira import JIRA
from datetime import datetime


class ATE_JIRA_X600:
    def __init__(self):
        self.jira_env_source = JIRA(basic_auth=('ProdATE', 'Ultra2009'), server='https://jira.ultratcs.ca')

    def create_new_radio_thermal_tests(self, ate_name: str, summary: str, work_order: str, radio_serial_number: str, assignee: str):
        issue_dict = {
            'project': 'X600T',
            'summary': summary,
            'assignee': {'name': assignee},
            'customfield_12205': ate_name,
            'customfield_12210': work_order,
            'customfield_12216': radio_serial_number,
            'issuetype': 'Thermal_Cycling_Tests',
        }
        issue = self.jira_env_source.create_issue(fields=issue_dict)
        print("New Radio: Thermal_cycling tests")
        return issue.key

    def get_thermal_tests_ticket_id(self, workorder: str, uut_serial_number: str):
        count = 0
        for singleIssue in self.jira_env_source.search_issues(jql_str='project = X600_Tests AND issuetype ="Thermal_Cycling_Tests" and work_order ~ "{}" and Radio_Serial_Number ~ "{}"'.format(workorder, uut_serial_number)):
            count = count + 1
        if count == 0:
            return "NotFound"
        else:
            return singleIssue.key

    def log_failed_loopback(self, ate_name: str, work_order: str, radio_serial_number: str, start_date: str, end_date: str, datasheet_path: str, assignee: str):
        thermal_tests_ticket_id = self.get_thermal_tests_ticket_id(work_order, radio_serial_number)
        if thermal_tests_ticket_id == "NotFound":
            thermal_tests_ticket_id = self.create_new_radio_thermal_tests(ate_name, "Thermal cycling | WorkOrder: {}| Radio SN: {}".format(work_order, radio_serial_number), work_order, radio_serial_number, assignee)
        # CREATE FAILED_ESS SUBTASK
        Failed_ess = self.jira_env_source.create_issue(
        project='X600T',
        summary='Loopback (Fail) | Date:{}'.format(datetime.now()),
        customfield_12216=radio_serial_number,
        customfield_12210=work_order,
        customfield_12218=start_date,
        customfield_12219=end_date,
        assignee={'name': assignee},
        issuetype={'name': 'Failed Loopback Thermal Cycling'},
        parent={'key': thermal_tests_ticket_id}
        )
        print("added a failed Loopback")
        # ATTACHE DATASHEET
        file = open(datasheet_path, 'rb')
        self.jira_env_source.add_attachment(issue=Failed_ess, attachment=file)
        # TRANSITION MAIN TICKET TO FAILED_ESS
        self.jira_env_source.transition_issue(thermal_tests_ticket_id, transition='FAILED_ESS')

    def log_failed_fail_free(self, ate_name: str, work_order: str, radio_serial_number: str, start_date: str, end_date: str, datasheet_path: str, assignee: str):
        thermal_tests_ticket_id = self.get_thermal_tests_ticket_id(work_order, radio_serial_number)
        if thermal_tests_ticket_id == "NotFound":
            thermal_tests_ticket_id = self.create_new_radio_thermal_tests(ate_name, "Thermal cycling | WorkOrder: {}| Radio SN: {}".format(work_order, radio_serial_number), work_order, radio_serial_number, assignee)
        # CREATE FAILED_ESS SUBTASK
        Failed_ess = self.jira_env_source.create_issue(
        project='X600T',
        summary='Fail Free (Fail) | Date:{}'.format(datetime.now()),
        customfield_12216=radio_serial_number,
        customfield_12210=work_order,
        customfield_12218=start_date,
        customfield_12219=end_date,
        assignee={'name': assignee},
        issuetype={'name': 'Failed Fail Free'},
        parent={'key': thermal_tests_ticket_id}
        )
        print("added a failed fail free")
        # ATTACHE DATASHEET
        file = open(datasheet_path, 'rb')
        self.jira_env_source.add_attachment(issue=Failed_ess, attachment=file)
        # TRANSITION MAIN TICKET TO FAILED_ESS
        self.jira_env_source.transition_issue(thermal_tests_ticket_id, transition='FAILED_ESS')

    def log_succesful_loopback(self, ate_name: str, work_order: str, radio_serial_number: str, start_date: str, end_date: str, datasheet_path: str):
        thermal_tests_ticket_id = self.get_thermal_tests_ticket_id(work_order, radio_serial_number)
        if thermal_tests_ticket_id == "NotFound":
            thermal_tests_ticket_id = self.create_new_radio_thermal_tests(ate_name, "Thermal cycling | WorkOrder: {}| Radio SN: {}".format(work_order, radio_serial_number), work_order, radio_serial_number)
        # CREATE SUCCESSFUL_ESS SUBTASK
        subtask = self.jira_env_source.create_issue(
        project='X600T',
        summary='Loopback (Pass) | Date:{}'.format(datetime.now()),
        customfield_12216=radio_serial_number,
        customfield_12210=work_order,
        customfield_12218=start_date,
        customfield_12219=end_date,
        issuetype={'name': 'Successful Loopback Thermal Cycling'},
        parent={'key': thermal_tests_ticket_id}
        )
        # ATTACHE DATASHEET
        file = open(datasheet_path, 'rb')
        self.jira_env_source.add_attachment(issue=subtask, attachment=file)
        print("added a successful Loopback")
        # AUTO CLOSE MAIN TICKET IF ALL FAILED_ESS HAS BEEN CLOSED
        all_failed_ess_are_closed = True
        for failed_ess in self.jira_env_source.search_issues(jql_str='project = X600_Tests AND (issuetype ="Failed Fail Free" OR issuetype ="Failed Loopback Thermal Cycling") and parent = "{}"'.format(thermal_tests_ticket_id)):
            if failed_ess.get_field('status') == "FAILED_ESS":
                all_failed_ess_are_closed = False
        if all_failed_ess_are_closed:
            self.jira_env_source.transition_issue(thermal_tests_ticket_id, transition='DONE')

    def log_succesful_fail_free(self, ate_name: str, work_order: str, radio_serial_number: str, start_date: str, end_date: str, datasheet_path: str):
        thermal_tests_ticket_id = self.get_thermal_tests_ticket_id(work_order, radio_serial_number)
        if thermal_tests_ticket_id == "NotFound":
            thermal_tests_ticket_id = self.create_new_radio_thermal_tests(ate_name, "Thermal cycling | WorkOrder: {}| Radio SN: {}".format(work_order, radio_serial_number), work_order, radio_serial_number)
        # CREATE SUCCESSFUL_ESS SUBTASK
        subtask = self.jira_env_source.create_issue(
        project='X600T',
        summary='Fail Free (Pass) | Date:{}'.format(datetime.now()),
        customfield_12216=radio_serial_number,
        customfield_12210=work_order,
        customfield_12218=start_date,
        customfield_12219=end_date,
        issuetype={'name': 'Successful Fail Free'},
        parent={'key': thermal_tests_ticket_id}
        )
        # ATTACHE DATASHEET
        file = open(datasheet_path, 'rb')
        self.jira_env_source.add_attachment(issue=subtask, attachment=file)
        print("added a successful Fail Free")
        # AUTO CLOSE MAIN TICKET IF ALL FAILED_ESS HAS BEEN CLOSED
        all_failed_ess_are_closed = True
        for failed_ess in self.jira_env_source.search_issues(jql_str='project = X600_Tests AND (issuetype ="Failed Fail Free" OR issuetype ="Failed Loopback Thermal Cycling") and parent = "{}"'.format(thermal_tests_ticket_id)):
            if failed_ess.get_field('status') == "FAILED_ESS":
                all_failed_ess_are_closed = False
        if all_failed_ess_are_closed:
            self.jira_env_source.transition_issue(thermal_tests_ticket_id, transition='DONE')

