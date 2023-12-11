def get_details():
    return dict(
        name='Account Created',
        description='Create account based on provided data',
        is_expandable=False,
        is_trigger=True,
        schema=dict(
            type='object',
            additionalProperties=False,
            description='Insert Row into BigQuery Table',
            required=['inputs', 'outputs'],
            properties=dict(
                expand_results=dict(
                    type='boolean',
                    default=False,
                    enum=[False]
                ),
                inputs=dict(
                    type='object',
                    additionalProperties=False,
                    required=["is_inherited"],
                    properties=dict(
                        is_inherited=dict(
                            type='boolean',
                            default=False
                        ),
                    )
                ),
                outputs=dict(
                    type='object',
                    required=[
                        'account_uuid'
                        'parent_uuids',
                        'name',
                        'created_ts'
                    ],
                    properties=dict(
                        account_uuid=dict(
                            type='string',
                        ),
                        parent_uuids=dict(
                            type='array',
                            items=dict(
                                type='string',
                                format='uuid'
                            )
                        ),
                        name=dict(
                            type='string'
                        ),
                        created_ts=dict(
                            type='integer',
                        )
                    )
                ),
            )
        )
    )


def process(workflow_uuid, account_uuid, node_uuid, trigger_uuid, ingested_ts, processed_ts, inputs, integration,
            **kwargs):
    pass
