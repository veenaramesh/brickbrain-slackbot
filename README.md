# BrickBrain

A Slackbot that brings BrickBrain Agent into Slack. We deploy the bot via a Databricks Apps. Users are able to ask questions, get responses from the agent, and provide feedback (via MLflow).

[For more information on BrickBrain](https://github.com/jiteshsoni/BrickBrain).

## Architecture

- **BrickBrain Agent** — Databricks Model Serving endpoint, created by Agent Bricks Knowledge Assistant
- **Traces and Feedback** — MLflow Tracking, where users can rate responses via a message shortcut

```markdown
┌─────────────┐      ┌──────────────────┐      ┌─────────────────────┐
│   Slack     │◄────►│  Databricks App  │◄────►│  Model Serving      │
│   Users     │      │  (Socket Mode)   │      │  (BrickBrain Agent) │
└─────────────┘      └──────────────────┘      └─────────────────────┘
                              │
                              ▼
                     ┌──────────────────┐
                     │  MLflow Tracking │
                     │  (Traces + Feedback)
                     └──────────────────┘
```

## Project Structure

```markdown
brickbrain_slackbot/
├── app/
│   ├── app.py              # Main Slack bot application
│   ├── app.yaml            # Databricks App configuration
│   ├── mlflow_client.py    # MLflow trace linking utilities
│   └── requirements.txt    # Python dependencies
├── notebooks/
│   └── LaunchApp.py        # Notebook to deploy the Databricks App
├── resources/              # DAB resource definitions
└── databricks.yml          # Databricks Asset Bundle configuration
```

## Configuration

### Environment Variables

The app expects the following environment variables (configured in `app.yaml`):

| Variable | Description |
|----------|-------------|
| `ENDPOINT_NAME` | Name of the Model Serving endpoint hosting BrickBrain |
| `EXPERIMENT_PATH` | MLflow experiment path for trace logging |
| `EXPERIMENT_ID` | MLflow experiment ID |

### Deployment Targets

Configured in `databricks.yml`:

| Target | Mode | Use Case |
|--------|------|----------|
| `dev` | development | Local development and testing |
| `stage` | development | Pre-production validation |
| `prod` | production | Production deployment |

## Deployment

### 1. Configure Secrets

Store your Slack bot token in Databricks:

```bash
databricks secrets put-secret brickbrain-scope slack-bot-token
```

### 2. Deploy with Databricks Asset Bundles

```bash
# Deploy to development
databricks bundle deploy -t dev

# Deploy to production
databricks bundle deploy -t prod
```

### 3. Launch the App

Run the `LaunchApp.py` notebook with parameters:
- `app_name`: Name for your Databricks App
- `ka_endpoint_name`: Your BrickBrain Model Serving endpoint name

## Usage

### Asking Questions

Simply message the bot in any channel it's invited to, or DM it directly. The bot will:
1. Retrieve conversation history from the thread
2. Send the context to the BrickBrain agent
3. Reply in the thread with the agent's response

### Providing Feedback

1. Right-click (or long-press) on any bot response
2. Select **Message shortcuts** → **Log Feedback**
3. Rate the response
4. Optionally add comments
5. Submit

Feedback is logged to MLflow and linked to the original trace for analysis.

## License

Internal use only.
