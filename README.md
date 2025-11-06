# iOS Bridge (DailyPilot app)

This folder will contain the notes and glue code that connect the DailyPilot-Engine
logic (Python reference implementation) to the DailyPilot iOS app.

High-level plan:

- Define a simple JSON contract between the iOS client and the engine.
- For early prototypes, run the engine as a local script during development.
- For production, re-implement the scoring and selection rules in Swift or expose
  the engine behind a small network service that the app can call.
