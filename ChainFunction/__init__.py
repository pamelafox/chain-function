import azure.functions as func

from ChainFunction.markov_chain import MarkovChain


def get_param(req, param_name):
    param_value = req.params.get(param_name)
    if not param_value:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            param_value = req_body.get(param_name)
    return param_value


def main(req: func.HttpRequest) -> func.HttpResponse:
    kind = get_param(req, "kind")
    chain = MarkovChain()
    if kind == "planet":
        chain.load_from_disk("ChainFunction/planet0825_2.pickle")
        return func.HttpResponse(chain.generate_planet(), status_code=200)
    elif kind:
        return func.HttpResponse(f"Unknown chain kind: {kind}", status_code=404)
    else:
        return func.HttpResponse("Chain kind not specified.", status_code=404)
