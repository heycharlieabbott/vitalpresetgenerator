import JSZip from 'jszip';
import wavetableData from './wavetable_data';
// Helper functions
const randomFloat = (min, max) => min + Math.random() * (max - min);
const randomBool = () => Math.random() < 0.5 ? 0 : 1;
const randomName = (length = 8) => {
  const chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
  return Array(length).fill(null).map(() => chars[Math.floor(Math.random() * chars.length)]).join('');
};

const generateRandomLFO = () => {
  const lfoShapes = [
    {
      name: "Triangle",
      num_points: 3,
      points: [0.0, 1.0, 0.5, 0.0, 1.0, 1.0],
      powers: [0.0, 0.0, 0.0],
      smooth: false
    },
    {
      name: "Saw Up",
      num_points: 3,
      points: [0.0, 1.0, 1.0, 0.0, 1.0, 1.0],
      powers: [0.0, 0.0, 0.0],
      smooth: false
    },
    {
      name: "Saw Down",
      num_points: 3,
      points: [0.0, 0.0, 1.0, 1.0, 1.0, 0.0],
      powers: [0.0, 0.0, 0.0],
      smooth: false
    },
    {
      name: "Bi polar Tri",
      num_points: 4,
      points: [0.0, 0.5, 0.25, 0.0, 0.75, 1.0, 1.0, 0.5],
      powers: [0.0, 0.0, 0.0, 0.0],
      smooth: false
    },
    {
      name: "Square",
      num_points: 4,
      points: [0.0, 1.0, 0.0, 1.0, 0.5, 0.0, 1.0, 1.0],
      powers: [0.0, 0.0, 0.0, 0.0],
      smooth: false
    }
  ];

  if (Math.random() < 0.7) {
    const baseShape = lfoShapes[Math.floor(Math.random() * lfoShapes.length)];
    const modifiedPoints = [];
    
    for (let i = 0; i < baseShape.points.length; i += 2) {
      modifiedPoints.push(baseShape.points[i]);
      modifiedPoints.push(baseShape.points[i + 1] + randomFloat(-0.1, 0.1));
    }
    
    return {
      name: baseShape.name,
      num_points: baseShape.num_points,
      points: modifiedPoints,
      powers: Array(baseShape.num_points).fill(null).map(() => randomFloat(-4.0, 4.0)),
      smooth: Math.random() < 0.5
    };
  }
  
  const numPoints = Math.floor(randomFloat(3, 9));
  const points = [];
  const xValues = Array(numPoints).fill(null).map(() => Math.random()).sort();
  xValues[0] = 0.0;
  xValues[xValues.length - 1] = 1.0;
  
  xValues.forEach(x => {
    points.push(x, Math.random());
  });
  
  return {
    name: `Custom ${Math.floor(Math.random() * 100)}`,
    num_points: numPoints,
    points,
    powers: Array(numPoints).fill(null).map(() => randomFloat(-4.0, 4.0)),
    smooth: Math.random() < 0.5
  };
};

const generateRandomWavetable = () => {
  const numKeyframes = Math.floor(randomFloat(2, 9));
  const positions = Array(numKeyframes).fill(null)
    .map(() => Math.floor(Math.random() * 257))
    .sort((a, b) => a - b);

  const keyframes = positions.map(pos => ({
    position: pos,
    start_position: randomFloat(0, 4000),
    window_fade: randomFloat(0.5, 1.0),
    window_size: Math.random() < 0.5 ? 1024 : 4096
  }));

  return {
    author: "",
    full_normalize: false,
    groups: [{
      components: [{
        audio_file: wavetableData.audio_file,
        audio_sample_rate: 44100,
        fade_style: 2,
        interpolation_style: 1,
        keyframes,
        normalize_gain: true,
        normalize_mult: false,
        phase_style: 2,
        random_seed: -919671038,
        type: "Audio File Source",
        window_size: 1012.9
      }]
    }],
    name: "fm sine",
    remove_all_dc: false,
    version: "1.5.5"
  };
};

const generateRandomModulation = (emptyModChance = 10) => {
  const destinations = [
    // Oscillator parameters
    ...[1, 2, 3].flatMap(i => [
      `osc_${i}_transpose`, `osc_${i}_tune`, `osc_${i}_level`, `osc_${i}_pan`,
      `osc_${i}_unison_detune`, `osc_${i}_unison_voices`, `osc_${i}_phase`,
      `osc_${i}_random_phase`, `osc_${i}_distortion_mix`, `osc_${i}_distortion_drive`,
      `osc_${i}_spectral_unison_method`, `osc_${i}_spectral_morph_amount`,
      `osc_${i}_spectral_unison_voices`, `osc_${i}_spectral_unison_amount`,
      `osc_${i}_wave_frame`, `osc_${i}_frame_spread`, `osc_${i}_frame_offset`
    ]),
    
    // LFO parameters
    ...[1, 2, 3, 4, 5, 6, 7, 8].flatMap(i => [
      `lfo_${i}_delay_time`, `lfo_${i}_fade_time`, `lfo_${i}_frequency`,
      `lfo_${i}_keytrack_transpose`, `lfo_${i}_keytrack_tune`, `lfo_${i}_phase`,
      `lfo_${i}_smooth_mode`, `lfo_${i}_smooth_time`, `lfo_${i}_stereo`
    ]),
    
    // Filter parameters
    ...[1, 2, 'fx'].flatMap(i => [
      `filter_${i}_blend`, `filter_${i}_blend_transpose`, `filter_${i}_cutoff`,
      `filter_${i}_drive`, `filter_${i}_filter_input`, `filter_${i}_formant_resonance`,
      `filter_${i}_formant_spread`, `filter_${i}_formant_transpose`, `filter_${i}_formant_x`,
      `filter_${i}_formant_y`, `filter_${i}_keytrack`, `filter_${i}_mix`, `filter_${i}_model`,
      `filter_${i}_on`, `filter_${i}_resonance`, `filter_${i}_style`
    ]),
    
    // Effects parameters
    'chorus_dry_wet', 'chorus_feedback', 'chorus_spread', 'chorus_delay_2',
    'chorus_delay_1', 'chorus_mod_depth', 'chorus_cutoff',
    'compressor_attack', 'compressor_high_gain', 'compressor_band_gain',
    'compressor_low_gain', 'compressor_mix', 'compressor_release',
    'delay_tempo', 'delay_dry_wet', 'delay_feedback', 'delay_filter_cutoff',
    'delay_filter_spread',
    'distortion_mix', 'distortion_filter_blend', 'distortion_drive',
    'distortion_filter_cutoff', 'distortion_filter_resonance',
    'eq_low_resonance', 'eq_low_cutoff', 'eq_low_gain',
    'flanger_dry_wet', 'flanger_mod_depth', 'flanger_feedback',
    'flanger_center', 'flanger_phase_offset', 'flanger_tempo',
    'phaser_dry_wet', 'phaser_feedback', 'phaser_mod_depth',
    'phaser_center', 'phaser_blend', 'phaser_tempo', 'phaser_phase_offset',
    'reverb_dry_wet', 'reverb_delay', 'reverb_chorus_amount',
    'reverb_low_shelf_cutoff', 'reverb_low_shelf_gain',
    'reverb_chorus_frequency', 'reverb_size', 'reverb_decay_time',
    'reverb_pre_high_cutoff',
    
    // Modulation parameters
    'modulation_3_amount', 'modulation_5_amount', 'modulation_6_amount',
    'modulation_7_amount', 'modulation_8_amount'
  ];

  const sources = [
    // Envelopes
    'env_1', 'env_2', 'env_3', 'env_4', 'env_5', 'env_6',
    // LFOs
    'lfo_1', 'lfo_2', 'lfo_3', 'lfo_4', 'lfo_5', 'lfo_6', 'lfo_7', 'lfo_8',
    // Macro controls
    'macro_control_1', 'macro_control_2', 'macro_control_3', 'macro_control_4',
    // Performance controls
    'note', 'velocity', 'mod_wheel', 'pitch_wheel', 'aftertouch', 'lift',
    'random', 'stereo'
  ];

  if (Math.random() * 100 < emptyModChance) {
    return { destination: "", source: "" };
  }

  return {
    destination: destinations[Math.floor(Math.random() * destinations.length)],
    source: sources[Math.floor(Math.random() * sources.length)]
  };
};

const getStyleRanges = (style) => {
  const ranges = {
    "Keys": {
      polyphony: [4, 32],
      osc_level: [0.6, 0.9],
      filter_cutoff: [40, 100],
      env_attack: [0.1, 0.5],
      env_decay: [0.4, 3.0],
      env_sustain: [0.4, 1.0],
      env_release: [0.3, 5.0]
    },
    "Bass": {
      polyphony: [1, 4],
      osc_level: [0.7, 1.0],
      filter_cutoff: [20, 80],
      env_attack: [0, 0.3],
      env_decay: [0.3, 3.0],
      env_sustain: [0.3, 1.0],
      env_release: [0.2, 6.0]
    },
    "Lead": {
      polyphony: [1, 4],
      osc_level: [0.6, 0.9],
      filter_cutoff: [40, 120],
      env_attack: [0, 3.0],
      env_decay: [0.3, 3.0],
      env_sustain: [0.4, 1.0],
      env_release: [0.2, 6.0]
    },
    "Pad": {
      polyphony: [4, 32],
      osc_level: [0.5, 0.8],
      filter_cutoff: [30, 90],
      env_attack: [0.5, 1.0],
      env_decay: [0.6, 1.0],
      env_sustain: [0.6, 1.0],
      env_release: [0.6, 1.0]
    },
    "Pluck": {
      polyphony: [4, 16],
      osc_level: [0.6, 0.9],
      filter_cutoff: [60, 120],
      env_attack: [0, 3.0],
      env_decay: [0.2, 6.0],
      env_sustain: [0, 1.0],
      env_release: [0.2, 0.4]
    },
    "FX": {
      polyphony: [1, 32],
      osc_level: [0.5, 1.0],
      filter_cutoff: [20, 120],
      env_attack: [0, 3.0],
      env_decay: [0.3, 6.0],
      env_sustain: [0, 1.0],
      env_release: [0.3, 1.0]
    },
    "Drums": {
      polyphony: [1, 8],
      osc_level: [0.7, 1.0],
      filter_cutoff: [60, 120],
      env_attack: [0, 0.1],
      env_decay: [0.1, 6.0],
      env_sustain: [0, 1.0],
      env_release: [0.1, 1.3]
    },
    "Sequence": {
      polyphony: [4, 16],
      osc_level: [0.6, 0.9],
      filter_cutoff: [40, 100],
      env_attack: [0, 1.0],
      env_decay: [0.2, 6.0],
      env_sustain: [0.2, 1.0],
      env_release: [0.2, 1.5]
    }
  };
  return ranges[style] || ranges["Keys"];
};

export const generateRandomPreset = (presetStyle = "Random") => {
  const presetStyles = ["Keys", "Bass", "Lead", "Pad", "Pluck", "FX", "Drums", "Sequence"];
  
  if (presetStyle === "Random") {
    presetStyle = presetStyles[Math.floor(Math.random() * presetStyles.length)];
  }
  
  const styleRanges = getStyleRanges(presetStyle);
  
  // Generate modulation settings
  const modulationSettings = {};
  for (let i = 1; i <= 64; i++) {
    modulationSettings[`modulation_${i}_amount`] = randomFloat(-1, 1);
    modulationSettings[`modulation_${i}_bipolar`] = randomBool();
    modulationSettings[`modulation_${i}_bypass`] = randomBool();
    modulationSettings[`modulation_${i}_power`] = randomFloat(-4, 4);
    modulationSettings[`modulation_${i}_stereo`] = randomBool();
  }

  const preset = {
    author: "RandomPresetGenerator",
    comments: "Randomly generated preset",
    macro1: randomName(),
    macro2: randomName(),
    macro3: randomName(),
    macro4: randomName(),
    preset_style: presetStyle,
    synth_version: "1.5.5",
    settings: {
      // Basic settings
      volume: 6000.0,
      polyphony: randomFloat(...styleRanges.polyphony),
      oversampling: 0.0,
      beats_per_minute: 2.0,
      bypass: 0.0,

      // Voice settings
      voice_amplitude: 1.0,
      voice_override: randomBool(),
      voice_priority: randomFloat(0, 8),
      voice_transpose: randomFloat(-24, 24),
      voice_tune: randomFloat(-1, 1),

      // Effect on/off states
      chorus_on: randomBool(),
      compressor_on: randomBool(),
      delay_on: randomBool(),
      distortion_on: randomBool(),
      eq_on: randomBool(),
      flanger_on: randomBool(),
      phaser_on: randomBool(),
      reverb_on: randomBool(),
      sample_on: randomBool(),

      // Filter on/off states
      filter_1_on: randomBool(),
      filter_2_on: randomBool(),
      filter_fx_on: randomBool(),

      // Oscillator settings
      ...[1, 2, 3].reduce((acc, i) => ({
        ...acc,
        [`osc_${i}_on`]: randomBool(),
        [`osc_${i}_level`]: randomFloat(...styleRanges.osc_level),
        [`osc_${i}_transpose`]: randomFloat(-24, 24),
        [`osc_${i}_tune`]: randomFloat(-1, 1),
        [`osc_${i}_unison_voices`]: Math.floor(randomFloat(1, 9)),
        [`osc_${i}_unison_detune`]: randomFloat(2, 5),
        [`osc_${i}_unison_blend`]: randomFloat(0.5, 1.0),
        [`osc_${i}_stereo_spread`]: randomFloat(0, 1),
        [`osc_${i}_random_phase`]: randomBool(),
        [`osc_${i}_phase`]: randomFloat(0, 1),
        [`osc_${i}_midi_track`]: 1,
        [`osc_${i}_distortion_type`]: Math.floor(randomFloat(0, 13)),
        [`osc_${i}_spectral_morph_type`]: Math.floor(randomFloat(0, 16)),
        [`osc_${i}_frame_spread`]: 0,
        [`osc_${i}_spectral_morph_amount`]: randomFloat(0, 1),
        [`osc_${i}_spectral_morph_phase`]: randomFloat(0, 1),
        [`osc_${i}_spectral_morph_spread`]: randomFloat(0, 1)
      }), {}),

      // Filter settings
      filter_1_cutoff: randomFloat(...styleRanges.filter_cutoff),
      filter_1_resonance: randomFloat(0, 1),
      filter_1_blend: randomFloat(0, 1),
      filter_1_style: Math.floor(randomFloat(0, 4)),
      filter_1_model: Math.floor(randomFloat(0, 9)),
      filter_1_drive: randomFloat(0, 1),
      filter_1_mix: randomFloat(0, 1),

      // Envelope settings
      ...[1, 2, 3, 4, 5, 6].reduce((acc, i) => ({
        ...acc,
        [`env_${i}_attack`]: randomFloat(...styleRanges.env_attack),
        [`env_${i}_decay`]: randomFloat(...styleRanges.env_decay),
        [`env_${i}_sustain`]: randomFloat(...styleRanges.env_sustain),
        [`env_${i}_release`]: randomFloat(...styleRanges.env_release),
        [`env_${i}_attack_power`]: randomFloat(-4, 4),
        [`env_${i}_decay_power`]: randomFloat(-4, 4),
        [`env_${i}_release_power`]: randomFloat(-4, 4)
      }), {}),

      // Effects
      reverb_decay_time: randomFloat(-5, 5),
      reverb_dry_wet: randomFloat(0, 1),
      reverb_size: randomFloat(0, 1),
      reverb_high_shelf_cutoff: randomFloat(20, 120),
      reverb_low_shelf_cutoff: randomFloat(0, 100),

      delay_feedback: randomFloat(0, 0.95),
      delay_dry_wet: randomFloat(0, 1),
      delay_tempo: Math.floor(randomFloat(2, 17)),

      // LFOs
      lfos: Array(8).fill(null).map(generateRandomLFO),

      // Modulations
      modulations: Array(64).fill(null).map(() => generateRandomModulation(70)),

      // Sample
      sample: {
        length: 0,
        name: "",
        sample_rate: 44100,
        samples: ""
      },

      // Wavetables
      wavetables: Array(3).fill(null).map(generateRandomWavetable),

      // Additional settings
      stereo_mode: randomBool(),
      pitch_bend_range: Math.floor(randomFloat(1, 25)),
      velocity_track: randomFloat(0, 1),
      portamento_time: randomFloat(-10, 0),
      legato: randomBool(),

      // Macro controls
      macro_control_1: randomFloat(0, 1),
      macro_control_2: randomFloat(0, 1),
      macro_control_3: randomFloat(0, 1),
      macro_control_4: randomFloat(0, 1),

      // Add all modulation settings
      ...modulationSettings
    }
  };

  return preset;
};

export const generateVitalbank = async (presets) => {
  const zip = new JSZip();
  const currentTime = new Date().toISOString().replace(/[-:]/g, '').split('.')[0];
  const folderName = `RANDOM_${currentTime}`;
  const presetsFolder = zip.folder(`${folderName}/Presets`);
  
  presets.forEach((preset) => {
    const presetName = `${randomName()}.vital`;
    presetsFolder.file(presetName, JSON.stringify(preset, null, 2));
  });
  
  return await zip.generateAsync({ type: "uint8array" });
}; 