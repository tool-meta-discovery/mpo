import L06Flask.Configuration
import L06Flask.Import
import L06Flask.Event
import L06Flask.Trace
import L06Flask.Algorithm
import L06Flask.Quality
import L06Flask.Optimization
import json


@L06Flask.Configuration.bp.after_request
@L06Flask.Import.bp.after_request
@L06Flask.Event.bp.after_request
@L06Flask.Trace.bp.after_request
@L06Flask.Algorithm.bp.after_request
@L06Flask.Quality.bp.after_request
@L06Flask.Optimization.bp.after_request
def after_request(response):
    response.data = json.dumps({"result": response.data.decode("utf-8")})
    return response
