import React, { useState } from "react";
import { generateRandomPreset, generateVitalbank } from "./lib/presetGenerator";

function App() {
  const [presetCount, setPresetCount] = useState(100);
  const [isGenerating, setIsGenerating] = useState(false);

  const handleDownload = async () => {
    try {
      setIsGenerating(true);
      // Generate presets and create a vitalbank
      const presets = Array(presetCount)
        .fill(null)
        .map(() => generateRandomPreset());
      const vitalbank = await generateVitalbank(presets);

      // Create a blob from the vitalbank data
      const blob = new Blob([vitalbank], { type: "application/octet-stream" });
      const url = window.URL.createObjectURL(blob);

      // Create a temporary link and trigger download
      const link = document.createElement("a");
      link.href = url;
      link.download = `random_presets_${Date.now()}.vitalbank`;
      document.body.appendChild(link);
      link.click();

      // Cleanup
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error("Error generating presets:", error);
      alert("Error generating presets. Please try again.");
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: "20px",
        padding: "20px",
        maxWidth: "1000px",
        margin: "0 auto",
      }}
    >
      <h1 style={{ color: "white" }}>Vital Preset Generator</h1>

      <div
        style={{
          color: "white",
          textAlign: "center",
          lineHeight: "1.6",
        }}
      >
        <p>
          This app generates random presets for the Vital synthesizer. Each
          preset includes randomized settings for oscillators, filters,
          envelopes, LFOs, and effects, creating unique and unexpected sounds.
          You can generate between 1 and 1000 presets at once, which will be
          packaged into a .vitalbank file that can be imported into Vital.
        </p>

        <div
          style={{
            backgroundColor: "#ff444422",
            border: "1px solid #ff6666",
            borderRadius: "8px",
            padding: "16px",
            margin: "20px 0",
            color: "#ff9999",
          }}
        >
          <strong>⚠️ Warning:</strong>
          <p style={{ margin: "8px 0 0 0" }}>
            Some generated presets have been found to cause Vital to crash when
            switching from the preset browser to the voices page or when
            switching presets directly on the voices page. Please save your work
            before auditioning new presets, and be cautious when navigating
            between pages while using generated presets.
          </p>
        </div>
      </div>

      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: "10px",
        }}
      >
        <label style={{ color: "white" }}>Number of Presets:</label>
        <input
          type="number"
          min="1"
          max="1000"
          value={presetCount}
          onChange={(e) =>
            setPresetCount(
              Math.max(1, Math.min(1000, parseInt(e.target.value) || 1))
            )
          }
          style={{
            padding: "8px",
            borderRadius: "4px",
            border: "1px solid #666",
            background: "#333",
            color: "white",
            width: "80px",
          }}
        />
      </div>
      <button
        onClick={handleDownload}
        disabled={isGenerating}
        style={{
          padding: "12px 24px",
          fontSize: "16px",
          borderRadius: "8px",
          border: "none",
          background: isGenerating ? "#555" : "#646cff",
          color: "white",
          cursor: isGenerating ? "not-allowed" : "pointer",
          transition: "background-color 0.3s",
        }}
      >
        {isGenerating ? "GENERATING..." : "DOWNLOAD"}
      </button>
    </div>
  );
}

export default App;
