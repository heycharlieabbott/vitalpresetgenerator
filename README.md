# Vital Preset Generator

A web application that generates random presets for the [Vital synthesizer](https://vital.audio/). This tool creates randomized preset banks that can be directly imported into Vital, offering a source of inspiration for sound design.

## Project History

This project exists in two versions:

1. The original Python script (`random_vital_preset.py`) - A command-line tool that served as the initial implementation and proof of concept
2. The current web application (JavaScript/React) - A more accessible version that provides the same functionality through a browser interface

The JavaScript implementation is a port of the Python code, maintaining the same preset generation logic while adding a user-friendly interface. Both versions produce compatible `.vitalbank` files that can be imported into Vital.

## Features

- Generate between 1 and 1000 random presets at once
- Presets are packaged into a `.vitalbank` file for easy importing
- Randomizes all major synthesis parameters:
  - Oscillator settings (levels, transposition, unison, etc.)
  - Filter configurations
  - Envelope parameters (ADSR)
  - LFO shapes and settings
  - Effect parameters
  - Modulation routings
- Style-based parameter ranges for different preset types:
  - Keys
  - Bass
  - Lead
  - Pad
  - Pluck
  - FX
  - Drums
  - Sequence

## ⚠️ Known Issues

**Important Warning**: Some generated presets have been found to cause Vital to crash when:

- Switching from the preset browser to the voices page
- Switching presets directly on the voices page

Please save your work before auditioning new presets and be cautious when navigating between pages while using generated presets.

## Usage Notes

1. Some generated presets might have:
   - All oscillators turned off by default
   - Very low volume levels
   - Filters that significantly reduce audible content
2. These presets are best used as starting points for your own sound design, rather than final sounds.

## Development

### Prerequisites

- Node.js (v14 or higher)
- npm

### Installation

1. Clone the repository:
   \`\`\`bash
   git clone https://github.com/yourusername/vitalpresetgenerator.git
   cd vitalpresetgenerator
   \`\`\`

2. Install dependencies:
   \`\`\`bash
   npm install
   \`\`\`

3. Start the development server:
   \`\`\`bash
   npm run dev
   \`\`\`

### Building for Production

To create a production build:
\`\`\`bash
npm run build
\`\`\`

## Technical Details

The application is built using:

- React
- Vite
- JSZip (for creating .vitalbank files)

The preset generation logic includes:

- Randomized LFO shape generation
- Style-based parameter range selection
- Wavetable configuration
- Modulation routing system

## License

MIT License - Feel free to use, modify, and distribute this code as you see fit.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
