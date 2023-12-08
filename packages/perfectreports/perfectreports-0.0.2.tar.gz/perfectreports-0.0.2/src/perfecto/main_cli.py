import time
from collections import Counter
import glob
from argparse import ArgumentParser
import datetime
import ssl
import numpy as np
import json
import os
import pandas
import json
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from py.functions import topFailedTC, format_df, hyperlink, prepare_failed_table, prepare_tags_table, topFailedReasons, prepare_module_graph, flatten_json, create_summary_pie, create_pie, get_report_details, df_formatter, prepare_device_coverage, get_resources, prepare_custom_failure_graph
from py.html import prepare_html

pandas.options.mode.copy_on_write = True

# Variables
reportTag = ""


def customReporter(client_logo, tags_to_remove, tags_to_skip_begins_with, tags_to_skip_ending_with, automation_owners, reportTag, loadCsv):
    truncated = True
    page = 1
    i = 0
    daysOlder = 0
    resources = []
    tags_df_table = ""
    tags_base64 = ""

    if loadCsv == "":
        resources = get_resources(
            truncated, reportTag, page, daysOlder, resources, jobName, jobNumber, startDate, endDate)

        if len(resources) > 0:
            # k = [q['tags'] for q in resources]
            # m = Counter(k)
            # print(m)
            # update tags
            for q in resources:
                q['tags'] = list(set(q['tags']) - set(tags_to_remove))
                q['tags'] = [x.replace("@", "") for x in q['tags']
                             if not x.startswith(tuple(tags_to_skip_begins_with)) if not x.endswith(tuple(tags_to_skip_ending_with))]
            jsonDump = json.dumps(resources)
            resources = json.loads(jsonDump)
            print("Total executions: " + str(len(resources)))
            df = pandas.DataFrame([flatten_json(x) for x in resources])

            # export df to csv
            df.to_csv("output.csv", index=False)
    else:
        df = pandas.read_csv(loadCsv, low_memory=False)

    if len(df) > 0:
        df = format_df(df, jobName, jobNumber, automation_owners)

        # async - don't put this below hyperlink
        topfailedtc_table = topFailedTC(df[(df["Test Status"] == "FAILED")])

        # based on descending end time, skiping if latest tests have passed
        trend_df = df.sort_values(by="endTime", ascending=False)
        first = trend_df.groupby('name').first()
        remove_names = first.drop(first[first["Test Status"] != "PASSED"].index)
        #Remove from trend_df the rows that matches the first names that passes.
        trend_df[~trend_df['name'].isin(remove_names.index.tolist())]
        #TODO test this for all available names
        print((trend_df[trend_df["name"] == 'AMT-105 - Extending Standing Order - Admin user']['Test Status'].value_counts(normalize=True) * 100).round(2))
        
        # hyperlinking name with report link
        df = hyperlink(df, "Result",
                       "reportURL", "name", "", False)

        passed = df[(df["Test Status"] == "PASSED")].shape[0]
        blocked = df[(df["Test Status"] == "BLOCKED")].shape[0]
        unknown = df[(df["Test Status"] == "UNKNOWN")].shape[0]
        failed_df = df[(df["Test Status"] == "FAILED")]
        failed = failed_df.shape[0]
        # prepare Device coverage
        df, version_items = prepare_device_coverage(df)

        execution_summary = {}
        df.replace(np.nan, '', regex=True)  # important to display all modules

        execution_summary = create_summary_pie(df, "", "Test Status", "count")
        # custom failure reason graph
        custom_failure_items = prepare_custom_failure_graph(failed_df)
        # module graph
        tags_base64 = prepare_module_graph(df)

        # replace failed in cleanException
        if not 'cleanException' in failed_df.columns:
            failure_items, custom_failure_items, failedTable, topfailedtc_table = "", "", "", ""
        else:
            failed_df['cleanException'] = failed_df['cleanException'].str.replace(
                r'\s+failed$|^Step\:And\s+|^Step\:Then\s+|^Step\:Given\s+|^Step\:When\s+', '', regex=True).astype('str')
            # clean error message
            failed_df = failed_df.reset_index()
            failed_df["message"] = failed_df["message"].fillna("-")
            failed_df['message'] = failed_df['message'].astype(
                'string').str.replace(r'Step.*\n|.*Error\:|.*Exception\:|\n.*|<[^>]+>|\.\.\.|.*\.xpath\:|.*\.cssSelector\:|.*intercepted\:(\s)+|(\s)+Other element.*|.*locate(\s)+element\:|.*reference\:|.*seconds\:', '', regex=True)

            # create table for failures
            failure_items = topFailedReasons(failed_df)

            failed_df = failed_df.rename(
                columns={
                    "cleanException": "Failed Step",
                    "message": "Failure Message",
                }
            )
            
            # pivot tags
            tags_df_table = prepare_tags_table(failed_df)
            
            failed_df['Failed Step'] = failed_df['Failed Step'].astype(
            'string').str.replace(r'<[^>]+>|\.\.\.', '', regex=True)

            # prepare failed table
            failedTable = prepare_failed_table(failed_df)

        strTable = prepare_html(client_logo, criteria, df.shape[0], passed, failed, unknown, blocked, execution_summary,
                                tags_base64, failure_items, custom_failure_items, version_items, tags_df_table, failedTable, topfailedtc_table)
        strTable = strTable.replace("<thead>", "<thead class='stuckHead'>")
        report_filename = "PerfectoReport.html"
        with open(report_filename, 'w') as f:
            f.write(strTable)
        print(
            "Report: file://"
            + os.path.join(os.getcwd(), report_filename)
        )


def main():
    tags_to_remove = ""
    tags_to_skip_begins_with = ""
    tags_to_skip_ending_with = ""
    automation_owners=""

    try:
        #     """fix Python SSL CERTIFICATE_VERIFY_FAILED"""
        if not os.environ.get("PYTHONHTTPSVERIFY", "") and getattr(
            ssl, "_create_unverified_context", None
        ):
            ssl._create_default_https_context = ssl._create_unverified_context
        parser = ArgumentParser(
            description="Perfecto Actions Reporter")
        parser.add_argument(
            "-c",
            "--cloud_name",
            metavar="cloud_name",
            help="Perfecto cloud name. (E.g. demo) or add it as a cloudName environment variable",
            nargs="?",
        )
        parser.add_argument(
            "-s",
            "--security_token",
            metavar="security_token",
            type=str,
            help="Perfecto Security Token/ Pass your Perfecto's username and password in user:password format  or add it as a securityToken environment variable",
            nargs="?",
        )
        parser.add_argument(
            "-r",
            "--report",
            type=str,
            metavar="prepares custom report",
            help="creates a custom report.",
            nargs="?",
        )
        parser.add_argument(
            "-l",
            "--logo",
            type=str,
            metavar="customer logo link",
            help="Customer logo link",
            nargs="?",
        )
        parser.add_argument(
            "-remove-tags",
            "--tags_to_remove",
            type=str,
            metavar="Remove Tags",
            help="Tags that needs to be removed from the results",
            nargs="?",
        )
        parser.add_argument(
            "-skip-tags-starting-with",
            "--tags_to_skip_begins_with",
            type=str,
            metavar="Remove Tags",
            help="Tags starting with certain characters that needs to be removed from the results",
            nargs="?",
        )
        parser.add_argument(
            "-skip-tags-ending-with",
            "--tags_to_skip_ending_with",
            type=str,
            metavar="Remove Tags",
            help="Tags starting with certain characters that needs to be removed from the results",
            nargs="?",
        )
        parser.add_argument(
            "-automation-owners",
            "--automation_owners",
            type=str,
            metavar="Automation Owners",
            help="JSON format of Automation Owners and modules",
            nargs="?",
        )
        

        args = vars(parser.parse_args())
        try:
            if not args["cloud_name"]:
                print("Loading cloudName: " +
                      os.environ["cloudName"] + " from environment variable.")
            else:
                os.environ["cloudName"] = args["cloud_name"]
        except Exception:
            if not args["cloud_name"]:
                parser.error(
                    "cloud_name parameter is empty. Either Pass the argument -c followed by cloud_name, eg. perfectoai -c demo or add it as a cloudName environment variable"
                )
                exit
            os.environ["cloudName"] = args["cloud_name"]
        try:
            if not args["security_token"]:
                print("Loading securityToken: " +
                      os.environ["securityToken"] + " from environment variable.")
            else:
                os.environ["securityToken"] = args["security_token"]
        except Exception:
            if not args["security_token"]:
                parser.error(
                    "security_token parameter is empty. Pass the argument -c followed by cloud_name, eg. perfectoai -c demo -s <<TOKEN>> || perfectoai -c demo -s <<user>>:<<password>> or add it as a securityToken environment variable"
                )
                exit
            os.environ["securityToken"] = args["security_token"]
        if args["logo"]:
            if str("www.").lower() not in str(args["logo"]).lower():
                raise Exception(
                    "Kindly provide valid client website url. Sample format: www.perfecto.io"
                )
                sys.exit(-1)
            client_logo = args["logo"]
        else:
            client_logo = "https://www.perforce.com/sites/default/themes/custom/perforce/logo.svg"

        if args["tags_to_remove"]:
            tags_to_remove = args["tags_to_remove"].split(",")

        if args["tags_to_skip_begins_with"]:
            tags_to_skip_begins_with = args["tags_to_skip_begins_with"].split(
                ",")
        if args["tags_to_skip_ending_with"]:
            tags_to_skip_ending_with = args["tags_to_skip_ending_with"].split(
                ",")
        if args["automation_owners"]:
            automation_owners = args["automation_owners"]

        try:
            global criteria
            global jobNumber
            global jobName
            global startDate
            global endDate
            loadCsv = ""
            jobName = ""
            jobNumber = ""
            startDate = ""
            endDate = ""
            temp = ""
            criteria = ""
            reportTag = ""
            report = args["report"]
            report_array = report.split("|")
            for item in report_array:
                if "report" in item:
                    report, criteria = get_report_details(
                        item, temp, "report", criteria
                    )
                if "jobName" in item:
                    jobName, criteria = get_report_details(
                        item, temp, "jobName", criteria
                    )
                if "jobNumber" in item:
                    jobNumber, criteria = get_report_details(
                        item, temp, "jobNumber", criteria
                    )
                if "startDate" in item:
                    startDate, criteria = get_report_details(
                        item, temp, "startDate", criteria
                    )
                if "endDate" in item:
                    endDate, criteria = get_report_details(
                        item, temp, "endDate", criteria
                    )
                if "reportTag" in item:
                    reportTag, criteria = get_report_details(
                        item, temp, "reportTag", criteria
                    )
                if "loadCsv" in item:
                    loadCsv, criteria = get_report_details(
                        item, temp, "loadCsv", criteria
                    )
        except Exception as e:
            raise Exception(
                "Verify parameters of report, split them by | seperator. Exception: " +
                str(e)
            )
            sys.exit(-1)
        filelist = glob.glob(os.path.join("*.html"))
        for f in filelist:
            os.remove(f)
        if jobName:
            criteria += "JOB: " + jobName.replace(";", "; ").upper() + ", "
        if jobNumber != "":
            criteria += "JOB#: " + \
                jobNumber.replace(";", "; ") + " "
        if reportTag != "":
            criteria += "TAG:" + str(reportTag).upper() + ", "
        if startDate != "":
            if "-" not in startDate:
                criteria += "START: " + str(datetime.datetime.strptime(str(datetime.fromtimestamp(int(int(startDate) / 1000))), "%Y-%m-%d %H:%M:%S")) + \
                    ", END: " + \
                    str(datetime.datetime.strptime(str(datetime.fromtimestamp(
                        int(int(endDate) / 1000))), "%Y-%m-%d %H:%M:%S"))
            else:
                criteria += "START: " + startDate + ", END: " + endDate
        customReporter(client_logo, tags_to_remove,
                       tags_to_skip_begins_with, tags_to_skip_ending_with, automation_owners, reportTag, loadCsv)

    except Exception as e:
        raise Exception("Oops!", e)


if __name__ == "__main__":
    start_time = datetime.datetime.now().replace(microsecond=0)
    main()
    end = datetime.datetime.now().replace(microsecond=0)
    print("Total Time taken:" + str(end - start_time))
    sys.exit()
