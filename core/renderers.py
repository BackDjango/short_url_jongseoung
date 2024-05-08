from rest_framework.renderers import JSONRenderer


class CustomRenderer(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response_data = renderer_context.get("response")

        try:
            status_code = response_data.status_code
            status_text = response_data.status_text
        except AttributeError:
            status_code = 200
            status_text = "OK"

        response = {
            "status_code": status_code,
            "status_text": status_text,
            "data": data,
        }
        return super(CustomRenderer, self).render(
            response, accepted_media_type, renderer_context
        )
