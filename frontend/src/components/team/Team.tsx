"use client";

import React from "react";
import { motion } from "framer-motion";
import Link from "next/link";
import Image from "next/image";
import { Github, Linkedin, Mail, Globe } from "lucide-react";

export interface TeamMember {
  name: string;
  role: string;
  affiliation?: string;
  bio?: string;
  image?: string;
  github?: string;
  linkedin?: string;
  email?: string;
  website?: string;
}

// ── Default Hackathon Team Data (Easily customize with teammates) ─────────────
export const TEAM_MEMBERS: TeamMember[] = [
  {
    name: "Wesley Kuria",
    role: "Lead Developer & Architect",
    affiliation: "Tone Core Engineering",
    bio: "Leading full-stack architecture, geospatial pipeline design, and AI-driven water intelligence models.",
    image: "", // Add photo URL or path in /public/images/
    github: "https://github.com/Wesley-Kuria",
    linkedin: "https://linkedin.com/",
    email: "wesley@example.com",
  },
  {
    name: "Teammate Name",
    role: "Full-Stack / Frontend Engineer",
    affiliation: "Tone Engineering",
    bio: "Building responsive visualization interfaces, MapLibre GL integrations, and real-time ROI modeling tools.",
    image: "",
    github: "https://github.com/",
    linkedin: "https://linkedin.com/",
    email: "teammate@example.com",
  },
  {
    name: "Teammate Name",
    role: "Data / AI Engineer",
    affiliation: "Tone Intelligence",
    bio: "Specializing in RAG pipelines, climate data synthesis, and automated prospect assessment briefs.",
    image: "",
    github: "https://github.com/",
    linkedin: "https://linkedin.com/",
    email: "teammate@example.com",
  },
];

const EASE: [number, number, number, number] = [0.25, 0.46, 0.45, 0.94];

const cardVariants = {
  hidden: { opacity: 0, y: 30 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.6, ease: EASE },
  },
};

const containerVariants = {
  hidden: {},
  visible: {
    transition: { staggerChildren: 0.12, delayChildren: 0.05 },
  },
};

interface TeamProps {
  title?: string;
  subtitle?: string;
  members?: TeamMember[];
  className?: string;
}

export default function Team({
  title = "Meet the Team Behind Tone",
  subtitle = "Built by a dedicated engineering team pioneering droplet-level water harvesting intelligence and resilient infrastructure.",
  members = TEAM_MEMBERS,
  className = "",
}: TeamProps) {
  return (
    <section id="team" className={`px-8 py-24 md:px-16 md:py-32 lg:px-24 ${className}`}>
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 24 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true, margin: "-60px" }}
        transition={{ duration: 0.7, ease: EASE }}
        className="text-center max-w-3xl mx-auto mb-16"
      >
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full border border-teal-500/20 bg-teal-500/10 text-teal-700 text-xs font-semibold uppercase tracking-widest mb-4">
          <span>💧 Hackathon Team</span>
        </div>
        <h2
          className="text-[42px] md:text-[56px] lg:text-[72px] leading-[1.05] tracking-[-1.5px] text-[#1a1a1a] mb-5"
          style={{ fontFamily: "var(--font-crimson), 'Crimson Text', Georgia, serif" }}
        >
          {title}
        </h2>
        <p className="text-[#64748b] text-[16px] leading-relaxed max-w-xl mx-auto">
          {subtitle}
        </p>
      </motion.div>

      {/* Team Cards Grid */}
      <motion.div
        variants={containerVariants}
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: "-60px" }}
        className={`grid gap-8 ${
          members.length === 1
            ? "max-w-md mx-auto"
            : members.length === 2
            ? "max-w-3xl mx-auto md:grid-cols-2"
            : "grid-cols-1 md:grid-cols-2 lg:grid-cols-3"
        }`}
      >
        {members.map((member, idx) => {
          const initials = member.name
            .split(" ")
            .map((n) => n[0])
            .join("")
            .slice(0, 2)
            .toUpperCase();

          return (
            <motion.div
              key={`${member.name}-${idx}`}
              variants={cardVariants}
              whileHover={{ y: -6, transition: { duration: 0.25 } }}
              className="group relative rounded-3xl border border-[#e2e8f0] bg-white/90 p-8 shadow-[0_4px_24px_rgba(15,23,42,0.04)] hover:shadow-[0_12px_40px_rgba(14,116,144,0.12)] hover:border-teal-500/30 transition-all duration-300 flex flex-col justify-between"
            >
              {/* Top Accent Gradient */}
              <div className="absolute top-0 left-8 right-8 h-1 bg-gradient-to-r from-teal-500 via-cyan-500 to-blue-500 rounded-b opacity-0 group-hover:opacity-100 transition-opacity duration-300" />

              <div>
                {/* Avatar */}
                <div className="relative mx-auto mb-6 h-32 w-32 overflow-hidden rounded-full bg-gradient-to-br from-teal-50 via-cyan-100 to-blue-100 ring-4 ring-teal-500/10 flex items-center justify-center shadow-inner">
                  {member.image ? (
                    <Image
                      src={member.image}
                      alt={member.name}
                      width={128}
                      height={128}
                      className="h-full w-full object-cover"
                    />
                  ) : (
                    <span
                      className="text-[38px] font-semibold text-teal-800 tracking-tight"
                      style={{ fontFamily: "var(--font-crimson), 'Crimson Text', Georgia, serif" }}
                    >
                      {initials}
                    </span>
                  )}
                </div>

                {/* Member Info */}
                <div className="text-center">
                  <h3
                    className="text-[26px] font-bold text-[#0f172a] leading-tight mb-1 tracking-tight"
                    style={{ fontFamily: "var(--font-crimson), 'Crimson Text', Georgia, serif" }}
                  >
                    {member.name}
                  </h3>

                  <div className="inline-block px-3 py-1 rounded-full bg-teal-50 border border-teal-200/60 text-teal-800 text-xs font-semibold tracking-wide mb-3">
                    {member.role}
                  </div>

                  {member.affiliation && (
                    <p className="text-[13px] font-medium text-[#64748b] mb-4">
                      {member.affiliation}
                    </p>
                  )}

                  {member.bio && (
                    <p className="text-[14px] text-[#475569] leading-relaxed mb-6 line-clamp-3">
                      {member.bio}
                    </p>
                  )}
                </div>
              </div>

              {/* Social Links */}
              <div className="pt-5 border-t border-slate-100 flex items-center justify-center gap-4 text-slate-400 group-hover:text-slate-600 transition-colors">
                {member.github && (
                  <Link
                    href={member.github}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="p-2 rounded-xl hover:bg-slate-100 hover:text-slate-900 transition-colors"
                    title="GitHub Profile"
                  >
                    <Github className="w-4 h-4" />
                  </Link>
                )}
                {member.linkedin && (
                  <Link
                    href={member.linkedin}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="p-2 rounded-xl hover:bg-blue-50 hover:text-blue-600 transition-colors"
                    title="LinkedIn Profile"
                  >
                    <Linkedin className="w-4 h-4" />
                  </Link>
                )}
                {member.email && (
                  <a
                    href={`mailto:${member.email}`}
                    className="p-2 rounded-xl hover:bg-teal-50 hover:text-teal-700 transition-colors"
                    title="Email"
                  >
                    <Mail className="w-4 h-4" />
                  </a>
                )}
                {member.website && (
                  <Link
                    href={member.website}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="p-2 rounded-xl hover:bg-cyan-50 hover:text-cyan-700 transition-colors"
                    title="Portfolio / Website"
                  >
                    <Globe className="w-4 h-4" />
                  </Link>
                )}
              </div>
            </motion.div>
          );
        })}
      </motion.div>
    </section>
  );
}
