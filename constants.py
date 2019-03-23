import signalFunctions as sgen

allFields = ['A', 't1', 'T', 'd', 'kw', 'fp', 'ts']
noise_fields = ['A', 't1', 'd', 'fp']
rectangular_fields = ['A', 'T', 't1', 'd', 'kw', 'fp']
unit_step = ['A', 't1', 'd', 'ts', 'fp']
sin_fields = ['A', 't1', 'T', 'd', 'fp']

signals={
    'uniform_noise': {
        'fn': sgen.uniform_noise,
        'fields': noise_fields,
    },
    'gaussian_noise': {
        'fn': sgen.gaussian_noise,
        'fields': noise_fields,
    },
    'sin': {
        'fn': sgen.sin,
        'fields': sin_fields,
    },
    'sin_half_rectified': {
        'fn': sgen.sin_half_rectified,
        'fields': sin_fields,
    },
    'sin_full_rectified': {
        'fn': sgen.sin_full_rectified,
        'fields': sin_fields,
    },
    'rectangular': {
        'fn': sgen.rectangular,
        'fields': rectangular_fields,
    },
    'rectangular_symmetrical': {
        'fn': sgen.rectangular_symmetrical,
        'fields': rectangular_fields,
    },
    'unit_step': {
        'fn': sgen.unit_step,
        'fields': unit_step
    },
    'sawtooth': {
        'fn': sgen.sawtooth,
        'fields': rectangular_fields
    }
}