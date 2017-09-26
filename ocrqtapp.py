# -*- coding: utf-8 -*-
from __future__ import print_function
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import editdistance
import diff_match_patch as dmp_module

app = Flask(__name__)
app.config.from_object(__name__)


@app.route("/", methods=['POST', 'GET'])
def index():

    cer_result = None
    htmldiff = None
    ground_truth_text = ""
    ocr_text=""
    ids = None
    messages = []
    ocr_precision = None

    if request.method == 'POST':
        if request.form['ground_truth_text'] and request.form['ocr_text']:

            # strip surrounding spacing
            ground_truth_text = request.form['ground_truth_text'].strip()
            ocr_text = request.form['ocr_text'].strip()

            #identical?
            if ground_truth_text == ocr_text:
                print("kjh" + ocr_text)
                cer=0.0
            else:
                # compute levenshtein / edit distance
                ids = editdistance.eval(ground_truth_text, ocr_text)
                cer = 100.0 * (ids/len(ground_truth_text))

                # diff output
                dmp = dmp_module.diff_match_patch()
                diffs = dmp.diff_main(ground_truth_text, ocr_text)
                htmldiff = dmp.diff_prettyHtml(diffs)
                
            cer_result = round(cer, 2)
            ocr_precision = round(100.0-cer, 2)

        else:
            # no data as input
            messages.append("Data saknas för beräkning. Ange text i båda fälten.")

    return render_template('index.html', messages=messages, htmldiff=htmldiff, gtlen=len(ground_truth_text), ocrlen=len(ocr_text),ids=ids, cer=cer_result, ocr_precision=ocr_precision, request=request)
