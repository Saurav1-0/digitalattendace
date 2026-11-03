"use client";

import { useState } from "react";

export default function Home() {
  const [activeTab, setActiveTab] = useState<"dashboard" | "upload" | "enrollment" | "gallery">("dashboard");

  // Sample data reflecting backend models and existing session_001 data
  const sampleStats = [
    { label: "Enrolled Students", value: "6", change: "+1 recently", color: "text-emerald-500" },
    { label: "Last Session", value: "session_001", change: "4 photos processed", color: "text-blue-500" },
    { label: "Faces Identified", value: "14", change: "Cosine threshold: 0.45", color: "text-indigo-500" },
    { label: "Needs Review", value: "1", change: "Margin < 0.05", color: "text-amber-500" },
  ];

  const recentDetections = [
    { id: "23105129023", name: "Student 23105129023", confidence: "0.68", evidenceCount: 3, status: "Present" },
    { id: "23105129044", name: "Student 23105129044", confidence: "0.61", evidenceCount: 2, status: "Present" },
    { id: "23105129059", name: "Student 23105129059", confidence: "0.74", evidenceCount: 4, status: "Present" },
    { id: "23105129060", name: "Student 23105129060", confidence: "0.58", evidenceCount: 2, status: "Present" },
    { id: "23105129089", name: "Student 23105129089", confidence: "0.49", evidenceCount: 1, status: "Review" },
    { id: "alok", name: "Alok", confidence: "0.79", evidenceCount: 4, status: "Present" },
  ];

  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-100 flex flex-col font-sans">
      {/* Navigation Header */}
      <header className="border-b border-zinc-800 bg-zinc-900/60 backdrop-blur sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-lg bg-emerald-500/20 border border-emerald-500/30 flex items-center justify-center text-emerald-400 font-bold">
              FM
            </div>
            <div>
              <h1 className="text-lg font-semibold tracking-tight text-white flex items-center gap-2">
                FaceMatch
                <span className="text-xs px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-medium">
                  YuNet + SFace
                </span>
              </h1>
              <p className="text-xs text-zinc-400">Digital Classroom Attendance System</p>
            </div>
          </div>

          {/* Navigation Tabs */}
          <nav className="flex items-center gap-1 bg-zinc-800/60 p-1 rounded-lg border border-zinc-700/50 text-sm">
            {(
              [
                { key: "dashboard", label: "Dashboard" },
                { key: "upload", label: "Take Attendance" },
                { key: "enrollment", label: "Enroll Student" },
                { key: "gallery", label: "Gallery" },
              ] as const
            ).map((tab) => (
              <button
                key={tab.key}
                onClick={() => setActiveTab(tab.key)}
                className={`px-3 py-1.5 rounded-md font-medium transition-all ${
                  activeTab === tab.key
                    ? "bg-zinc-700 text-white shadow-sm"
                    : "text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800/40"
                }`}
              >
                {tab.label}
              </button>
            ))}
          </nav>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
        {/* Metric Cards */}
        <section className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {sampleStats.map((stat, i) => (
            <div
              key={i}
              className="p-5 rounded-xl bg-zinc-900 border border-zinc-800 hover:border-zinc-700 transition flex flex-col justify-between"
            >
              <span className="text-xs font-medium uppercase tracking-wider text-zinc-400">
                {stat.label}
              </span>
              <div className="my-2">
                <span className={`text-3xl font-bold tracking-tight ${stat.color}`}>
                  {stat.value}
                </span>
              </div>
              <span className="text-xs text-zinc-500">{stat.change}</span>
            </div>
          ))}
        </section>

        {/* Dashboard View */}
        {activeTab === "dashboard" && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Attendance Session Summary */}
            <div className="lg:col-span-2 rounded-xl bg-zinc-900 border border-zinc-800 p-6 space-y-6">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-lg font-semibold text-white">Latest Attendance Roster</h2>
                  <p className="text-sm text-zinc-400">
                    Provisional results from multi-angle classroom scan
                  </p>
                </div>
                <button
                  onClick={() => setActiveTab("upload")}
                  className="px-3.5 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-sm font-medium transition shadow"
                >
                  New Scan
                </button>
              </div>

              {/* Roster Table */}
              <div className="overflow-x-auto">
                <table className="w-full text-left text-sm">
                  <thead className="text-xs uppercase bg-zinc-800/50 text-zinc-400 border-y border-zinc-800">
                    <tr>
                      <th className="py-3 px-4">Student ID</th>
                      <th className="py-3 px-4">Evidence Count</th>
                      <th className="py-3 px-4">Match Score</th>
                      <th className="py-3 px-4">Attendance Status</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-zinc-800/60">
                    {recentDetections.map((row) => (
                      <tr key={row.id} className="hover:bg-zinc-800/30 transition">
                        <td className="py-3 px-4 font-mono font-medium text-zinc-200">
                          {row.id}
                        </td>
                        <td className="py-3 px-4 text-zinc-400">
                          {row.evidenceCount} photos
                        </td>
                        <td className="py-3 px-4 text-zinc-300 font-mono">
                          {row.confidence}
                        </td>
                        <td className="py-3 px-4">
                          <span
                            className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-semibold ${
                              row.status === "Present"
                                ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20"
                                : "bg-amber-500/10 text-amber-400 border border-amber-500/20"
                            }`}
                          >
                            {row.status}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Pipeline Configuration & Status */}
            <div className="rounded-xl bg-zinc-900 border border-zinc-800 p-6 space-y-5">
              <h2 className="text-lg font-semibold text-white">AI Engine Status</h2>
              <div className="space-y-3 text-sm">
                <div className="flex items-center justify-between p-3 rounded-lg bg-zinc-800/40 border border-zinc-800">
                  <span className="text-zinc-400">Face Detector</span>
                  <span className="font-mono text-zinc-200">YuNet (ONNX)</span>
                </div>
                <div className="flex items-center justify-between p-3 rounded-lg bg-zinc-800/40 border border-zinc-800">
                  <span className="text-zinc-400">Face Recognizer</span>
                  <span className="font-mono text-zinc-200">SFace (128D)</span>
                </div>
                <div className="flex items-center justify-between p-3 rounded-lg bg-zinc-800/40 border border-zinc-800">
                  <span className="text-zinc-400">Cosine Threshold</span>
                  <span className="font-mono text-zinc-200">0.45</span>
                </div>
                <div className="flex items-center justify-between p-3 rounded-lg bg-zinc-800/40 border border-zinc-800">
                  <span className="text-zinc-400">Ambiguity Margin</span>
                  <span className="font-mono text-zinc-200">0.05</span>
                </div>
                <div className="flex items-center justify-between p-3 rounded-lg bg-zinc-800/40 border border-zinc-800">
                  <span className="text-zinc-400">Gallery File</span>
                  <span className="font-mono text-xs text-emerald-400">student_gallery.npz</span>
                </div>
              </div>

              <div className="pt-3 border-t border-zinc-800 text-xs text-zinc-500">
                Backend connection endpoint: <code className="text-zinc-400">http://127.0.0.1:8000</code>
              </div>
            </div>
          </div>
        )}

        {/* Attendance Upload View */}
        {activeTab === "upload" && (
          <div className="rounded-xl bg-zinc-900 border border-zinc-800 p-8 space-y-6 max-w-3xl mx-auto">
            <div>
              <h2 className="text-xl font-bold text-white">Process Classroom Photographs</h2>
              <p className="text-sm text-zinc-400 mt-1">
                Upload one or multiple classroom images from different angles to compute multi-frame attendance.
              </p>
            </div>

            <div className="border-2 border-dashed border-zinc-700 hover:border-zinc-500 rounded-xl p-10 text-center flex flex-col items-center justify-center transition cursor-pointer bg-zinc-800/20">
              <svg className="w-12 h-12 text-zinc-500 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M3 15a4 4 0 004 4h10a4 4 0 004-4M3 15a4 4 0 014-4h1.5a1.5 1.5 0 001.06-.44l1.88-1.88A1.5 1.5 0 0112.5 8H14a1.5 1.5 0 011.06.44l1.88 1.88a1.5 1.5 0 001.06.44H19a4 4 0 014 4M3 15l4-4m14 4l-4-4" />
              </svg>
              <p className="text-sm font-medium text-zinc-300">Click to select photos or drag & drop</p>
              <p className="text-xs text-zinc-500 mt-1">JPG, JPEG, PNG, WEBP files supported</p>
            </div>

            <div className="flex justify-end gap-3 pt-4 border-t border-zinc-800">
              <button
                onClick={() => setActiveTab("dashboard")}
                className="px-4 py-2 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-zinc-300 text-sm font-medium transition"
              >
                Cancel
              </button>
              <button className="px-5 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-sm font-medium transition shadow">
                Run Face Detection & Matching
              </button>
            </div>
          </div>
        )}

        {/* Student Enrollment View */}
        {activeTab === "enrollment" && (
          <div className="rounded-xl bg-zinc-900 border border-zinc-800 p-8 space-y-6 max-w-2xl mx-auto">
            <div>
              <h2 className="text-xl font-bold text-white">Enroll New Student</h2>
              <p className="text-sm text-zinc-400 mt-1">
                Add student reference portraits. Images must have exactly 1 clear front-facing face.
              </p>
            </div>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-zinc-300 mb-1">
                  Student Roll / Registration ID
                </label>
                <input
                  type="text"
                  placeholder="e.g. 23105129099"
                  className="w-full px-4 py-2 rounded-lg bg-zinc-800 border border-zinc-700 focus:outline-none focus:border-emerald-500 text-white text-sm"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-zinc-300 mb-1">
                  Reference Portrait
                </label>
                <div className="border border-dashed border-zinc-700 rounded-lg p-6 text-center text-sm text-zinc-400">
                  Upload portrait (1 person in image)
                </div>
              </div>
            </div>

            <div className="flex justify-end gap-3 pt-4 border-t border-zinc-800">
              <button
                onClick={() => setActiveTab("dashboard")}
                className="px-4 py-2 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-zinc-300 text-sm font-medium transition"
              >
                Cancel
              </button>
              <button className="px-5 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-sm font-medium transition shadow">
                Generate & Save Embedding
              </button>
            </div>
          </div>
        )}

        {/* Gallery View */}
        {activeTab === "gallery" && (
          <div className="rounded-xl bg-zinc-900 border border-zinc-800 p-6 space-y-6">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-xl font-bold text-white">Student Face Gallery</h2>
                <p className="text-sm text-zinc-400">
                  Enrolled reference dataset in <code className="text-emerald-400">backend/data/student_gallery.npz</code>
                </p>
              </div>
              <button
                onClick={() => setActiveTab("enrollment")}
                className="px-4 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-sm font-medium transition shadow"
              >
                + Add Student
              </button>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-4">
              {["23105129023", "23105129044", "23105129059", "23105129060", "23105129089", "alok"].map((id) => (
                <div key={id} className="p-4 rounded-xl bg-zinc-800/40 border border-zinc-800 text-center space-y-2">
                  <div className="w-14 h-14 rounded-full bg-zinc-700/60 mx-auto flex items-center justify-center text-zinc-300 font-semibold text-sm">
                    {id.slice(-3)}
                  </div>
                  <div className="font-mono text-xs text-zinc-200 truncate">{id}</div>
                  <div className="text-[11px] text-emerald-400 font-medium">Embedding Ready</div>
                </div>
              ))}
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-zinc-800 py-4 text-center text-xs text-zinc-500">
        FaceMatch Digital Attendance &bull; Next.js 16 + React 19 + Tailwind CSS
      </footer>
    </div>
  );
}
