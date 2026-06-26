# Simulator ID Selection Implementation Plan

Status: In Progress

## Goal

Make automatic iOS simulator discovery unambiguous without changing caller-supplied destination or simulator-name overrides.

## Tasks

1. Add a failing portable contract for duplicate simulator names.
2. Add a POSIX AWK selector for the first available iPhone UDID.
3. Use the selected UDID in the automatic Xcode destination.
4. Document the default behavior and maintenance result.
5. Run local checks and hosted Apple-platform tests.
