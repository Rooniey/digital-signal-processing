import signalFunctions as sgen

allFields = ['A', 't1', 'T', 'd', 'kw', 'fp', 'ts', 'p']
noise_fields = ['A', 't1', 'd', 'fp']
rectangular_fields = ['A', 'T', 't1', 'd', 'kw', 'fp']
unit_step = ['A', 't1', 'd', 'ts', 'fp']
sin_fields = ['A', 't1', 'T', 'd', 'fp']
unit_impulse = ['A', 't1', 'd', 'fp', 'ts']
impulse_noise = ['A', 't1', 'd', 'fp', 'p']

signals={
    'uniform_noise': {
        'fn': sgen.uniform_noise,
        'fields': noise_fields,
        'isDiscrete': True,
        'isPeriodic': False
    },
    'gaussian_noise': {
        'fn': sgen.gaussian_noise,
        'fields': noise_fields,
        'isDiscrete': True,
        'isPeriodic': False
    },
    'sin': {
        'fn': sgen.sin,
        'fields': sin_fields,
        'isDiscrete': False,
        'isPeriodic': True
    },
    'sin_half_rectified': {
        'fn': sgen.sin_half_rectified,
        'fields': sin_fields,
        'isDiscrete': False,
        'isPeriodic': True
    },
    'sin_full_rectified': {
        'fn': sgen.sin_full_rectified,
        'fields': sin_fields,
        'isDiscrete': False,
        'isPeriodic': True
    },
    'rectangular': {
        'fn': sgen.rectangular,
        'fields': rectangular_fields,
        'isDiscrete': False,
        'isPeriodic': True
    },
    'rectangular_symmetrical': {
        'fn': sgen.rectangular_symmetrical,
        'fields': rectangular_fields,
        'isDiscrete': False,
        'isPeriodic': True
    },
    'unit_step': {
        'fn': sgen.unit_step,
        'fields': unit_step,
        'isDiscrete': False,
        'isPeriodic': False
    },
    'sawtooth': {
        'fn': sgen.sawtooth,
        'fields': rectangular_fields,
        'isDiscrete': False,
        'isPeriodic': True
    },
    'unit_impulse': {
        'fn': sgen.unit_impulse,
        'fields': unit_impulse,
        'isDiscrete': True,
        'isPeriodic': False,
    },
    'impulse_noise': {
        'fn': sgen.impulse_noise,
        'fields': impulse_noise,
        'isDiscrete': True,
        'isPeriodic': False,
    }
}