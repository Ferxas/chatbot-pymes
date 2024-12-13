def register_routes(api):
    from app.routes.foda import FODAResource
    from app.routes.predictions import PredictionsResource
    from app.routes.marketing import MarketingResource
    
    # register endpoints
    
    api.add_resource(FODAResource, '/api/foda')
    api.add_resource(PredictionsResource, '/api/predictions')
    api.add_resource(MarketingResource, '/api/marketing')
    