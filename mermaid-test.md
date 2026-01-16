```mermaid
graph TD
    A[Start] --> B{Process Step};
    B -->|Yes| C[End];
    B -->|No| D[Retry];
    D --> A;