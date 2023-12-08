
def prepare_html(client_logo, criteria, total, passed, failed, unknown, blocked, execution_summary,
                 tags_base64, failure_items, custom_failure_items, version_items, tags_df_table, failedTable, topfailedtc_table):
    html = str('''
<!DOCTYPE html>
<script src="http://code.jquery.com/jquery-1.11.0.min.js"></script>
<html>

<head>
    <style>
    
        html {
            display:inline-grid;
        }
        
        body {
            font-family: sans-serif;
            font-size: 11px;
            margin: 0px;
            background: #f0f7f7bf;
        }

        .option2 {
            text-indent: 15px;
            display: inline-block;
            padding-right: 28px;
            text-align: right;
            margin: -4px;
            border-radius: 1em;
        }

        .stuckHead {
            position: sticky;
            top: 0;
            z-index: 1;
        }

        table,
        th,
        td {
            border: 0px solid black;
            border-collapse: collapse;
            font-size: 11px;
        }

        .options2 {
            opacity: .8;
        }

        table.center {
            margin-left: auto;
            margin-right: auto;
        }

        th,
        td {
            padding: 2px;
            font-weight: 100;
        }

        th {
            text-align: center;
            box-sizing: border-box;
            border: 2px solid #366e9936;
            font-size: 12px;
            background: #5e90d8;
            font-weight: 600;
            color: white;
            text-align: center;
            line-height: 150%;
            vertical-align: middle;
        }

        td {
            box-sizing: border-box;
            border: 2px solid #366e9936;
            position: relative;
            color: #200302;
            background: #ffffff;
            vertical-align: middle;
            font-size: 11px;
            line-height: 140%;
            text-align: left;
        }

        img {
            display: inline-flex;
            height: 100%;
        }

        #summary {
            text-align: center;
            background: #f0ffff;
        }

        ::-webkit-scrollbar {
            -webkit-appearance: none;
            width: 5px;
            height: 5px;
        }

        ::-webkit-scrollbar-thumb {
            border-radius: 2px;
            background-color: rgba(0, 0, 0, .5);
            box-shadow: 0 0 1px rgba(255, 255, 255, .5);
        }

        #piechart,
        #browserChart {
            background-color: rgba(238, 240, 223, 0.68);
            display: block;
            width: 300px;
            height: 240px;
            margin: 5px;
            box-shadow: 0 0 60px rgb(80 130 50 / 33%);
        }

        #table tr td:nth-child(2) {
            max-width: 76px;
        }
        
        #table tr td:nth-child(3) {
            max-width: 200px;
        }

        #table tr td:nth-child(4){
            width: 40px;
        } 
        
        #table tr td:nth-child(5) {
            max-width: 150px;
        }
        
        #table tr td:nth-child(6) {
          max-width: 120px;
        }
      
        #input1 {
            background-image: url(https://img.icons8.com/color/48/search--v1.png);
            background-position: 1px 0px;
            background-repeat: no-repeat;
            background-size: 10px 15px;
            height: auto;
            font-size: 12px;
            padding: 0px 1px 0px 20px;
            margin-left: 10px;
            box-shadow: 0 0 80px rgba(2, 112, 0, 0.4);
        }

        #images {
            background: linear-gradient(to right, #ffb35a70, #E3F3FE, #E3F3FE, #aacfe8 90.33%, #ffb35a70);
            box-shadow: 0 1px 6px rgba(0, 0, 0, 0.12), 0 1px 4px rgba(0, 0, 0, 0.24);
            height: 35px;
            margin: auto;
            display: flex;
            justify-content: center;
            padding: 2px 1px 2px 10px;
        }

        #mas {
            width: 100px;
            padding-left: 20px;
        }

        #perfecto {
            width: 100px;
        }

        #criteria-legend {
            box-shadow: 0 1px 6px rgba(0, 0, 0, 0.12), 0 1px 4px rgba(0, 0, 0, 0.24);
            background: #78d9e891;
            background-image: linear-gradient(#78d9e891, #d9f0f491, #ffffffc2);
            padding: 5px;
            display: flex;
            justify-content: center;
            padding-top: 9px;
        }

        #summary-legend {
            box-shadow: 0 1px 6px rgba(0, 0, 0, 0.12), 0 1px 4px rgba(0, 0, 0, 0.24);
            background: #ffb35a70;
            padding: 5px;
        }

        #table {
            box-shadow: 0 10px 10px rgb(80 130 50 / 33%);
            overflow-y: scroll;
            word-wrap: break-word;
            margin-top: 0px;
            max-height: 500px;
            width: 770px;
        }

        #moduleheading {
            overflow: scroll;
            height: 210px;
            max-width: 400px;
        }

        #hie {
            display: flex;
            flex-wrap: wrap;
            flex-direction: column;
            align-content: center;
        }

        .option2 {
            font-size: small;
        }
        
        #vidlink {
            background-image: url(https://img.icons8.com/office/16/link.png);
            background-position: 2px 0px;
            background-repeat: no-repeat;
            height: 16px;
            width: 18px;
        }

        #tags,
        #topfailedtests, #topfailedmessages {
            overflow-y: scroll;
            word-wrap: break-word;
            display: inline-block;
            border-collapse: collapse;
            table-layout: fixed;
            max-height: 260px;
        }

        #tags tbody tr th,
        #topfailedtests tbody tr th, #topfailedtests tbody tr th, #topfailedtests tbody tr,
        #topfailedmessages tbody tr th, #topfailedmessages tbody tr th, #topfailedmessages tbody tr {
            text-align: left;
            background: #fffaf2;
            color: black;
            font-weight: 100;
            font-size: 10px;
        }

        #topfailedtests tbody tr th,
        #topfailedmessages tbody tr th {
            width: 200px !important;
        }

        #topfailedtests tbody tr td:nth-child(1),
        #topfailedmessages tbody tr td:nth-child(1) {
          min-width: 350px; 
        }

        #tags thead tr:nth-child(1) {
            display: none;
        }

        #slide {
            display: inline-flex;
            background: #f8ffff;
            flex-direction: row;
            overflow: scroll;
            align-items: self-start;
            justify-content: flex-start;
        }

        a {
            color: #04192d;
        }

        #heading {
            font-size: small;
            display: flex;
            flex-direction: row;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            width: 100%;
            padding: 5px 0;
            text-align: center;
            cursor: pointer;
            color: white;
            background: #002e5dd1;
            height: 15px;
        }

        svg {
            overflow: scroll;
        }

        #box {
            box-shadow: 0 -4px 18px 0 rgba(60, 118, 191, 0.55);
            margin-right: 2px;
            margin-left: 2px;
            margin-top: 3px;
            border: 1px solid #89def77d;
        }

        #topfailbox {
            margin: 3px;
            max-height: 310px;
            width: 380px;
            overflow: scroll;
            display: inline-table;
        }
        
        #reporticon {
            padding-left: 20px;   
        }
    </style>
</head>
<title>Perfecto Summary Report</title>

<body>
    <div id="images">
        <img src='https://cdn.brandfolder.io/UEOJKODA/at/ntbjr5wtnmb66b7pkj8rw23/logo-perfecto.auto?height=57&width=200'
            alt="Perfecto" id="perfecto" class="center">
        <img src="''' + client_logo + '''" alt="mas" id="mas" class="center">
        <img width="40" height="35" src="https://img.icons8.com/fluency/48/graph-report.png" id="reporticon"  alt="graph-report"/>
    </div>
    <div id="criteria-legend">
        <h2 class="option2" style="background-color: #ffd7aed4;">''' + str(criteria) + '''</h2>
        <h2 class="option2" style="background-color: lightgoldenrodyellow;">''' + str(total) + ''' \nTESTS</h2>
        <h2 class="option2" style="background-color:#33d63391;">''' + str(passed) + ''' \nPASSED</h2>
        <h2 class="option2" style="background-color:#ff5f41b5;">''' + str(failed) + ''' \nFAILED</h2>
        <h2 class="option2" style="background-color:#f2ebeb;">''' + str(unknown) + ''' \nUNKNOWNS</h2>
        <h2 class="option2" style="background-color:orange">''' + str(blocked) + ''' \nBLOCKED</h2>
    </div>
    <div id="summary">
        <div id="slide">
            <div id="box"><div id="heading">Overall Status</div>''' + execution_summary + '''</div></div>
            <div id="box"><div id="heading">Module-wise Status</div><div id="moduleheading">''' + tags_base64 + '''</div></div>
            ''' + version_items + ''' 
            <div id="box"><div id="heading">Top 5 Custom Failure Reasons</div><div>''' + custom_failure_items + '''</div></div>
        </div>
    </div>
    <div id="summary">
        <div id="slide">
            <div id="topfailbox">
                <div id="heading">Top 5</div>
                <div id="tagsheading">''' + failure_items + '''</div>
                <div id="tagsheading">''' + topfailedtc_table + '''</div>
                <div id="tagsheading">''' + tags_df_table + '''</div>
            </div>
            <div id="box">
                <div id="heading">Failed Tests Summary <input id="input1" type="text" placeholder="Search/Filter.."></input>
                </div>
                <div id="table">''' + failedTable + '''</div>
            </div>
        </div>
    </div>
</body>

<script>
    $(document).ready(function(){ 
        $("#tags thead tr:nth-child(2) th:nth-child(4)")[0].innerText = "Σ";
        $("#table thead tr th:nth-child(4)")[0].style.fontSize = "smaller";
    });
    
    document.getElementById('input1').addEventListener('keyup', debound(filter_table, 500))

    function filter_table(e) {
        const rows = document.querySelectorAll('#table tbody tr')
        rows.forEach(row => {
            row.style.display = (row.innerText.toLowerCase().includes(e.target.value.toLowerCase())) ? '' : 'none'
        })
    }

    function debound(func, timeout) {
        let timer
        return (...args) => {
            if (!timer) {
                func.apply(this, args);
            }
            clearTimeout(timer)
            timer = setTimeout(() => {
                func.apply(this, args)
                timer = undefined
            }, timeout)
        }
    }
</script>

</html>
        ''')
    return html
