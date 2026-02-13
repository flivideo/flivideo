# ElevenLabs Voice Agent Best Practices Guide

**Last Updated:** 2026-02-10

A comprehensive guide to building robust voice agents with ElevenLabs based on official documentation, community resources, and production experience.

---

## Table of Contents

1. [Official SDK Versions](#official-sdk-versions)
2. [WebRTC vs WebSocket](#webrtc-vs-websocket)
3. [Audio Quality & Feedback Prevention](#audio-quality--feedback-prevention)
4. [Client Tools Implementation](#client-tools-implementation)
5. [Connection Management](#connection-management)
6. [Conversation Mode & Interruptions](#conversation-mode--interruptions)
7. [System Prompt Best Practices](#system-prompt-best-practices)
8. [Voice Settings Configuration](#voice-settings-configuration)
9. [Model Selection Guidelines](#model-selection-guidelines)
10. [Knowledge Base & RAG Integration](#knowledge-base--rag-integration)
11. [Debug Mode & Event Logging](#debug-mode--event-logging)
12. [Production Deployment Checklist](#production-deployment-checklist)
13. [Common Issues & Solutions](#common-issues--solutions)

---

## Official SDK Versions

### Latest Versions (as of 2026-02-10)

- **@elevenlabs/react**: v0.14.0 (published 4 days ago)
- **Python SDK**: Requires Python >=3.9.0
- **LiveKit Integration**: Requires livekit-plugins-elevenlabs

### Installation

```bash
# React SDK
npm i @elevenlabs/react

# Python SDK
pip install elevenlabs

# LiveKit Plugin
pip install livekit-plugins-elevenlabs
```

**Key Compatibility:**
- React SDK supports WebRTC and WebSocket connections
- Swift SDK has WebRTC support
- React Native and Android SDK WebRTC support coming soon
- LiveKit integration supports both TTS and STT

---

## WebRTC vs WebSocket

### Official Recommendation: **Use WebRTC**

ElevenLabs has migrated all usage on 11.ai to WebRTC with dramatically improved client SDK performance and conversation quality.

### Why WebRTC?

**Audio Quality Benefits:**
- Best-in-class echo cancellation (battle-tested across billions of video calls)
- Superior background noise removal
- Prevents audio feedback issues inherently
- Native browser support in all modern browsers

**Performance:**
- Better latency characteristics
- More stable connections
- Built-in network adaptation

### Implementation

```typescript
// React SDK - WebRTC is default
const conversation = useConversation({
  // WebRTC connection automatically used
});
```

**Migration Path:**
- WebRTC support available now in npm package as alternative to WebSocket
- Swift SDK has WebRTC support
- No code changes required when using latest SDKs

---

## Audio Quality & Feedback Prevention

### Audio Constraints (Critical)

**Official ElevenLabs Configuration:**

```typescript
const audioConstraints = {
  echoCancellation: true,
  noiseSuppression: true,
  autoGainControl: true,
};
```

These settings are used when accessing the microphone through the browser's MediaDevices API.

### Audio Feedback Prevention

**Primary Strategy:** WebRTC's built-in echo cancellation handles most feedback issues automatically.

**Additional Techniques:**
- **Recording Pause During Speech**: Pause microphone input while agent is speaking
- **Browser Constraints**: Use the recommended audio constraints above
- **VAD Configuration**: Voice Activity Detection helps prevent unwanted audio pickup

### Audio Quality Optimization

**For Voice Clones:**
- Compress training audio to reduce dynamic range
- Target RMS: -23 dB to -18 dB
- True peak: below -3 dB
- Avoid background noise, low-frequency energy, and volume inconsistencies

**For Conversations:**
- Most natural conversations: 0.9-1.1x speed
- Slower for complex topics
- Faster for routine information

---

## Client Tools Implementation

### Setup Process

1. **Configure in ElevenLabs UI:**
   - Navigate to Tools section
   - Click "Add Tool"
   - Set Tool Type to "Client"
   - Define name, description, and parameters

2. **Register in Code:**

```typescript
const clientTools = {
  // Tool name must match UI configuration EXACTLY (case-sensitive)
  get_weather: async (params: { location: string }) => {
    // Async execution supported
    const result = await fetchWeather(params.location);
    return result;
  },

  update_ui: (params: { action: string }) => {
    // Synchronous execution also supported
    return { success: true };
  }
};

const conversation = useConversation({
  clientTools,
});
```

### Critical Requirements

**Case-Sensitive Matching:**
- Tool names in code MUST match UI configuration exactly
- Parameter names MUST match exactly

**Wait for Response:**
- Enable "Wait for response" in UI if agent should receive data back
- Agent will pause and wait for tool completion
- Response appends to conversation context

**Tool States:**
Tools can be in one of four states:
- `loading`: Tool is executing
- `awaiting_approval`: Waiting for user approval
- `success`: Tool completed successfully
- `failure`: Tool execution failed

### Async Tool Registration (Python)

```python
from elevenlabs import ClientTools

# Register async tool
client_tools = ClientTools()
client_tools.register(
    "get_weather",
    get_weather_async,
    is_async=True
)

# Custom event loop (if needed)
client_tools = ClientTools(loop=custom_loop)
```

### Best Practices

**1. Clear Instructions in System Prompt:**
Providing clear instructions significantly improves tool calling accuracy.

**2. Model Selection:**
When using tools, pick high intelligence models:
- ✅ GPT-4o mini
- ✅ Claude 3.5 Sonnet
- ❌ Avoid Gemini 1.5 Flash

**3. Error Handling:**
```typescript
const clientTools = {
  risky_operation: async (params) => {
    try {
      const result = await performOperation(params);
      return { success: true, data: result };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }
};
```

**4. Timeout Handling:**
Set appropriate timeouts for long-running operations.

---

## Connection Management

### Token Authentication

**Token Expiration:**
- Single-use tokens expire after **15 minutes**
- Signed WebSocket URLs expire after **15 minutes**
- Active WebSocket connections are NOT closed when token expires
- Creating new connections with expired tokens will fail

**Token Refresh Strategy:**
```typescript
// No built-in refresh - generate new token when needed
async function getNewToken() {
  const response = await fetch('/api/elevenlabs/token');
  return response.json();
}

// Monitor connection and refresh token proactively
useEffect(() => {
  const refreshInterval = setInterval(() => {
    // Refresh token every 14 minutes (before 15min expiration)
    refreshToken();
  }, 14 * 60 * 1000);

  return () => clearInterval(refreshInterval);
}, []);
```

### Session Configuration

```typescript
const conversation = useConversation({
  // One of these is required:
  signedUrl: 'wss://...',        // Signed WebSocket URL
  conversationToken: 'token...',  // Conversation token
  agentId: 'agent-id',            // Agent ID

  // Recommended: Map to your users
  userId: 'user-123',

  // Optional configurations
  serverLocation: 'us',           // 'us', 'eu-residency', 'in-residency', 'global'
  textOnly: false,                // Chat mode
  useWakeLock: true,              // Prevent device sleep (default: true)
});
```

### Wake Lock (Prevent Sleep)

**Default Behavior:**
Conversation automatically acquires wake lock to prevent device sleep.

**Disable Wake Lock:**
```typescript
const conversation = useConversation({
  useWakeLock: false,
});
```

**Browser Support:**
- Chrome, Edge, Opera: ✅ Full support
- Safari: ⚠️ May have limitations
- Requires HTTPS

### Connection Status Monitoring

```typescript
const conversation = useConversation({
  onStatusChange: (status) => {
    console.log('Connection status:', status);
    // Handle: connecting, connected, disconnected
  },

  onError: (error) => {
    console.error('Connection error:', error);
    // Implement retry logic
  },
});
```

### Retry Strategy

**LLM Fallback Cascade:**
```typescript
// In agent configuration
{
  cascade_timeout_seconds: 8,  // Wait before cascading to next LLM
  // Range: 2-15 seconds (default: 8)
}
```

---

## Conversation Mode & Interruptions

### Mode Change Detection

```typescript
const conversation = useConversation({
  onModeChange: (mode) => {
    // mode: 'SPEAKING' | 'LISTENING'
    console.log('Agent is now:', mode);

    // Update UI indicator
    setIsSpeaking(mode === 'SPEAKING');
  },
});
```

### Turn Eagerness

Controls how quickly assistant interprets pauses as opportunities to respond.

**Available Modes:**

1. **Eager:**
   - Responds quickly, jumps in at earliest opportunity
   - Best for: Fast-paced conversations, quick responses
   - Use case: Customer service, quick Q&A

2. **Normal (Recommended):**
   - Balanced turn-taking
   - Best for: Most conversational scenarios
   - Waits for natural conversation breaks

3. **Patient:**
   - Waits longer before taking turn
   - Best for: Collecting detailed information
   - Use case: Forms, surveys, complex information gathering

### Timeout Configuration

**Turn Timeout:**
```typescript
{
  timeout_duration: 10,  // seconds
  // Range: 1-30 seconds
  // How long to wait in silence before prompting user
}
```

**Soft Timeout:**
```typescript
{
  use_llm_generated_message: true,  // Generate contextual timeout message
  // vs predefined timeout message
}
```

**Best Practices:**
- **Customer Service**: 5-10s timeout + interruptions enabled + eager turn-taking
- **Legal/Compliance**: 15-30s timeout + interruptions disabled + normal turn-taking
- **Technical Support**: 10-15s timeout + normal turn-taking

### Handling Interruptions

**Shorter timeouts (5-10s) with interruptions enabled:**
Allow customers to interject with questions during agent responses.

**Longer timeouts (15-30s) with interruptions disabled:**
Ensure full delivery of important information without user interruption.

### User Activity Signal

```typescript
// Notify agent of user activity to prevent interruptions
conversation.sendUserActivity();

// Example: User is typing
inputElement.addEventListener('input', () => {
  conversation.sendUserActivity();
  // Agent pauses speaking for ~2 seconds
});
```

---

## System Prompt Best Practices

### Fundamentals

A system prompt is the **personality and policy blueprint** of your AI agent. It defines:
- Agent's role and goals
- Allowable tools
- Step-by-step instructions
- Guardrails (what agent should NOT do)

### Spelling Normalization for Voice Transcription

**Critical for brand names with non-standard spelling:**

Voice transcription may mishear words that sound different from how they're spelled. Add explicit spelling normalization rules to your system prompt:

```markdown
# Spelling Normalization (CRITICAL)

When you receive user input or transcriptions, automatically normalize these product names to their correct spelling:

**Fli-branded products** (all spelled F-L-I, NOT F-L-Y):
- When you see/hear "FlyHub" or "Fly Hub" → Normalize to "FliHub"
- When you see/hear "FlyVideo" or "Fly Video" → Normalize to "FliVideo"
- When you see/hear "FlyGen" or "Fly Gen" → Normalize to "FliGen"
- When you see/hear "FlyDeck" or "Fly Deck" → Normalize to "FliDeck"
- When you see/hear "FlyVoice" or "Fly Voice" → Normalize to "FliVoice"

**Why:** These product names sound like "fly" when spoken, but are always spelled "Fli" (F-L-I).

**Important:** Use the correct "Fli" spelling in:
- Your responses to the user
- Tool call parameters (especially in search queries)
- All references to these products

Example:
- User says: "Jump to Fly Hub folder"
- You understand: "Jump to FliHub"
- Tool call: jumpSearch(query="FliHub")
- Response: "I found FliHub and opened it in Finder for you."
```

**When to use:**
- Brand names with non-phonetic spelling
- Technical terms that sound different from spelling
- Acronyms with specific pronunciation
- Product names that users speak incorrectly

### Structure Template

```
# Role and Personality
You are a [role] who [characteristics].

# Tone and Style
[Concise tone description - only define once, don't repeat]

# Objectives
1. [Primary objective]
2. [Secondary objective]

# Guardrails
[Non-negotiable rules - models pay extra attention to this heading]
- Do not [forbidden action]
- Never [forbidden action]
- Always [required action]

# Instructions
[Step-by-step procedures]
This step is important: [critical step]

# Character Normalization
When collecting structured data (emails, phone numbers, codes):
- Normalize to spoken format: "john at company dot com"
- Maintain correct written format for tools

# Examples
[Provide examples for complex formatting, multi-step processes, edge cases]
```

### Best Practices

**1. Define Tone Once:**
```
✅ Good: "You are a friendly customer service agent who speaks in concise, clear, empathetic sentences."

❌ Bad: Repeating tone guidance throughout prompt
```

**2. Highlight Critical Steps:**
```
Verify user identity before proceeding. This step is important.
```

**3. Repeat Most Important Rules:**
Repeat the 1-2 most critical instructions twice in the prompt.

**4. Use Knowledge Base:**
Ground responses in factual information to prevent hallucinations.

**5. Keep Responses Concise:**
```
Answer succinctly in a couple of sentences and let the user guide you on where to give more detail.
```

**6. Design for Natural Language:**
Users are more verbose when talking than typing. Handle longer, conversational inputs.

### Example: Customer Service Agent

```
# Role
You are a friendly airline customer service agent helping passengers with flight issues.

# Tone
Speak in concise, clear, empathetic sentences.

# Guardrails
- Never make promises about refunds without supervisor approval
- Do not share other passengers' information
- Always verify passenger identity before discussing booking details

# Instructions
1. Greet the passenger warmly
2. Ask for booking reference
3. Verify identity with name and email. This step is important.
4. Listen to their concern
5. Offer solutions based on available tools
6. Summarize next steps before ending call

# Knowledge Base
Use the flight policy knowledge base for refund and rebooking rules.
```

---

## Voice Settings Configuration

### Key Parameters

**Stability:**
- Controls voice consistency and emotional range
- **Low (0.30-0.50)**: More emotional, dynamic delivery (may sound unstable)
- **High (0.60-0.85)**: Consistent, monotonous output
- ⚠️ Too low: Overly random, speaks too quickly
- ⚠️ Too high: Limited emotion

**Similarity:**
- Controls how closely AI adheres to original voice
- **Lower**: More variation from original
- **Higher**: Closer to original (may reproduce artifacts if source is poor quality)

**Style Exaggeration:**
- Amplifies style of original speaker
- Setting > 0 increases computational resources and latency
- **Default**: 0 (recommended for most use cases)

### Common Settings (Recommended)

```typescript
{
  stability: 50,           // Balanced
  similarity: 75,          // Close to original
  style_exaggeration: 0,   // Minimal latency
}
```

### Voice Speed

Most natural conversations: **0.9-1.1x speed**
- Adjust slower for complex topics
- Adjust faster for routine information

### Testing Voice Settings

1. Use same prompt with different voice settings
2. Run agent through various conversation scenarios
3. Test both text-based and voice interactions
4. Fine-tune speech clarity, pacing, and tone

---

## Model Selection Guidelines

### Available Models

- Gemini 1.5 Flash / Gemini 1.5 Pro
- GPT-4o Mini / GPT-4o / GPT-4o Turbo
- Claude 3.5 Sonnet / Claude 3.7 Sonnet / Claude Sonnet 4
- Claude 3 Haiku
- Custom LLM (OpenAI-compatible API)

### Recommendations by Use Case

**Complex Tasks & Reasoning:**
- ✅ **Claude 3.7 Sonnet** or **Claude Sonnet 4**
- Superior reasoning, reduced hallucinations
- Ideal for nuanced understanding

**General Performance:**
- ✅ **GPT-4o**
- Strong general performance
- Multimodal capabilities

**Speed & Low Latency:**
- ✅ **Gemini Flash 2.0**
- Best rapid responses
- Lowest latency
- Great for tool use

**When Using Tools:**
- ✅ **GPT-4o mini** or **Claude 3.5 Sonnet**
- ❌ **Avoid Gemini 1.5 Flash** (poor tool performance)

**Custom Fine-Tuned Models:**
Connect any OpenAI-compatible API for specialized use cases.

---

## Knowledge Base & RAG Integration

### What is RAG?

Retrieval-Augmented Generation enables agents to access large knowledge bases during conversations.

**Benefits:**
- Access knowledge bases larger than prompt limits
- More accurate, knowledge-grounded responses
- Reduce hallucinations by referencing source material
- Scale knowledge without creating multiple specialized agents

### How It Works

1. **Query Processing:** User question analyzed and reformulated for optimal retrieval
2. **Retrieval:** System finds most semantically similar content from knowledge base
3. **Response Generation:** Agent generates response using conversation context + retrieved information

### Performance

ElevenLabs' architecture: **50% faster RAG latency**
- Old: 326ms median latency
- New: 155ms median latency

### Setup

1. Navigate to agent's settings
2. Go to Knowledge Base section
3. Toggle on "Use RAG"

**Note:** RAG option only appears once knowledge base reaches size where retrieval is more efficient than direct inclusion.

### Automatic Indexing

- Documents automatically indexed when added to agent with RAG enabled
- No manual indexing required

### Best Practices

1. **Specialized Agents:**
   - Each agent should have narrow, clearly defined knowledge base
   - Fewer edge cases
   - Clearer success criteria
   - Faster response times

2. **Knowledge Base Content:**
   - Add content directly on ElevenLabs Agents platform
   - Content becomes available during conversations
   - Keep knowledge base focused and relevant

---

## Debug Mode & Event Logging

### Debug Events

```typescript
const conversation = useConversation({
  onDebug: (debugInfo) => {
    console.log('Debug event:', debugInfo);
    // Includes: tentative responses, internal events
    // Useful for development and troubleshooting
  },
});
```

### Message Events

```typescript
const conversation = useConversation({
  onMessage: (message) => {
    console.log('Message:', message);
    // Types:
    // - Tentative/final user voice transcription
    // - LLM replies
    // - Debug messages (when debug enabled)
  },
});
```

### Available Event Handlers

```typescript
const conversation = useConversation({
  onMessage: (msg) => {},              // New message received
  onError: (error) => {},              // Error encountered
  onAudio: (audio) => {},              // Audio data received
  onModeChange: (mode) => {},          // Speaking/listening mode change
  onStatusChange: (status) => {},      // Connection status change
  onCanSendFeedbackChange: (can) => {},// Feedback capability change
  onDebug: (debug) => {},              // Debug information
  onUnhandledClientToolCall: (call) => {}, // Unhandled client tool
  onVadScore: (score) => {},           // Voice activity detection score
  onAudioAlignment: (data) => {},      // Audio alignment data
});
```

### Enable Events in Agent Settings

⚠️ If callback enabled but events not coming through:
1. Go to ElevenLabs dashboard
2. Navigate to agent settings
3. Open "Advanced" tab
4. Enable corresponding events

### Real-Time Monitoring

Client events facilitate real-time communication:
- Audio delivery
- Transcription
- Agent responses
- System notifications

Events are automatically handled by SDKs but can be intercepted for advanced implementations.

---

## Production Deployment Checklist

### Security Best Practices

**1. Environment Separation:**
- ✅ Never mix test and production data
- ✅ Use separate agents for dev/staging/production

**2. Secret Management:**
- ✅ Use ElevenLabs platform secret management for API keys
- ✅ Never commit credentials to version control
- ✅ Store tokens securely server-side

**3. Access Control:**
- ✅ Enable SSO (Okta, Azure AD, Google Workspace)
- ✅ Implement RBAC (Role-Based Access Control)
- ✅ Use workspace roles to manage permissions

**4. Tool Approval:**
- ✅ Use "Always Ask" mode for maximum security with MCP tools
- ✅ Require explicit approval for sensitive operations

**5. Data Protection:**
- ✅ Enable Zero Retention Mode (enterprise feature)
- ✅ Use end-to-end encryption
- ✅ SOC2 and GDPR compliant

### Pre-Production Validation

**1. Safety Testing:**
- Define red teaming tests aligned with safety framework
- Conduct manual test calls using safety scenarios
- Set evaluation criteria for safety performance
- Run simulations with structured prompts
- Review and iterate until consistent results

**2. Performance Testing:**
- Test conversation scenarios (happy path, edge cases)
- Verify tool execution reliability
- Measure latency and response times
- Test voice quality across different settings

**3. Gradual Rollout:**
- Start with small user percentage
- Monitor safety performance continuously
- Increase rollout as metrics improve

### Runtime Configuration

**Conversation Overrides:**

⚠️ **Security Requirement:** Enable conversation overrides in agent security settings before using.

```typescript
const conversation = useConversation({
  overrides: {
    systemPrompt: 'Custom prompt for this user...',
    firstMessage: 'Hello, welcome back!',
    language: 'es',
    voice: 'custom-voice-id',
    llm: 'gpt-4o',
  },
});
```

**Server Location (Data Residency):**
```typescript
serverLocation: 'eu-residency',  // 'us', 'eu-residency', 'in-residency', 'global'
```

All conversation data and audio streams remain within specified geographic region.

### Webhook Integration

**Post-Call Webhooks:**
- Transcription webhooks (full conversation data)
- Audio webhooks (base64-encoded audio)
- Call initiation failure webhooks

**Authentication:**
- HMAC signatures for webhook verification
- Securely store shared secret

**Reliability:**
- Auto-disabled after 10+ consecutive failures (if no success in 7+ days)
- Return HTTP 200 quickly to indicate receipt
- Validate signature before processing

### Browser Compatibility

**Supported Browsers:**
- ✅ Chrome (recommended)
- ✅ Firefox
- ✅ Edge
- ⚠️ Safari (may have issues on older versions)

**Testing Strategy:**
Test features across multiple browsers as JavaScript handling varies.

---

## Common Issues & Solutions

### Voice Quality Issues

**Problem:** Voice drops in volume, whispers, or distorts

**Solution:**
- Adjust voice settings (Stability slider)
- Compress training audio to reduce dynamic range
- Target RMS: -23 dB to -18 dB
- True peak: below -3 dB

**Problem:** Inconsistency and voice variability

**Solution:**
- Use multilingual v2 model (less prominent issue)
- Clone voice with consistent samples
- Remove background noise from training audio
- Avoid low-frequency energy bursts

**Problem:** Language switching mid-generation

**Solution:**
- Use Instant Voice Clone or Professional Voice Clone
- Ensure high-quality, consistent training audio
- Use Studio feature for additional stability
- Break text into sections under 800 characters

### Audio Degradation

**Problem:** Quality degrades during extended TTS conversions

**Solution:**
- Break text into sections under 800 characters
- Especially important with Multilingual v1 model

### Corrupt Speech

**Problem:** Muffled, strange-sounding speech

**Solution:**
- Rare issue, usually resolves by regenerating
- No specific solution - retry generation

### Connection Issues

**Problem:** WebSocket "already in CLOSING or CLOSED state" error

**Solution:**
- Status cycles: Disconnected → Connected → Disconnected
- Check token expiration (15 minutes)
- Implement token refresh before expiration
- Monitor connection status and implement retry logic

**Problem:** React Native permission error

**Solution:**
- Explain microphone access to users in UI
- Request permission before Conversation starts
- Check if microphone blocked by browser/OS
- Verify development build is available

### Agent Performance Issues

**Problem:** Agent provides incorrect information

**Solution:**
- Review conversation transcripts with low satisfaction
- Strengthen specific sections of system prompt
- Add examples for edge cases
- Improve tool error handling

**Problem:** Agent fails to understand user intent

**Solution:**
- Add examples to system prompt
- Simplify language
- Test with more natural, verbose inputs

**Problem:** Agent breaks character

**Solution:**
- Add guardrails for edge cases
- Review and strengthen personality section
- Test with diverse conversation scenarios

**Problem:** Tools fail frequently

**Solution:**
- Improve error handling in tool implementation
- Better parameter descriptions
- Use high-intelligence models (GPT-4o mini, Claude 3.5 Sonnet)

### Conversation Flow Issues

**Faster Response Generation:**
Assistant starts speaking after receiving enough words + comma, rather than waiting for complete sentences. This reduces latency and creates more responsive conversations.

---

## Agent Configuration via API

### When Claude Code Skills Are Not Enough

**Important Distinction:**
- **agents skill (informational only)** - Provides documentation, cannot make API calls
- **Direct API calls (operational)** - Actually updates agent configuration

**Use Case:** When you need to programmatically update agent configuration (system prompt, tools, voice settings), you must use direct API calls.

### Python Script for Agent Updates

```python
#!/usr/bin/env python3
import requests

AGENT_ID = "agent_xxxxxxxxxxxxx"
API_KEY = "sk_xxxxxxxxxxxxxxxx"
BASE_URL = "https://api.elevenlabs.io/v1"

headers = {
    "xi-api-key": API_KEY,
    "Content-Type": "application/json"
}

payload = {
    "conversation_config": {
        "agent": {
            "prompt": {
                "prompt": """Your updated system prompt here..."""
            }
        }
    }
}

response = requests.patch(
    f"{BASE_URL}/convai/agents/{AGENT_ID}",
    headers=headers,
    json=payload
)

if response.status_code == 200:
    print("✅ Agent updated successfully!")
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)
```

**When to use this approach:**
- Updating system prompts programmatically
- Adding spelling normalization rules
- Batch updates to multiple agents
- Automation workflows

**When NOT to use this:**
- For exploring documentation (use agents skill)
- For understanding ElevenLabs concepts (use agents skill)
- For one-time manual config changes (use dashboard)

## Additional Resources

### Official Documentation
- [React SDK Documentation](https://elevenlabs.io/docs/agents-platform/libraries/react)
- [Client Tools Guide](https://elevenlabs.io/docs/agents-platform/customization/tools/client-tools)
- [Prompting Guide](https://elevenlabs.io/docs/agents-platform/best-practices/prompting-guide)
- [Voice Design Guide](https://elevenlabs.io/docs/agents-platform/customization/voice/best-practices/conversational-voice-design)

### Official Blog Posts
- [ElevenLabs Conversational AI WebRTC](https://elevenlabs.io/blog/conversational-ai-webrtc)
- [Building an Effective Voice Agent](https://elevenlabs.io/blog/building-an-agent-for-our-own-docs)
- [Conversational AI 2.0](https://elevenlabs.io/blog/conversational-ai-2-0)
- [How We Engineered RAG to be 50% Faster](https://elevenlabs.io/blog/engineering-rag)

### Community Resources
- [GitHub: elevenlabs/packages](https://github.com/elevenlabs/packages)
- [GitHub: elevenlabs/elevenlabs-examples](https://github.com/elevenlabs/elevenlabs-examples)
- [NPM: @elevenlabs/react](https://www.npmjs.com/package/@elevenlabs/react)

### Related Guides
- [Building Conversational AI Chatbots with TTS](https://elevenlabs.io/blog/best-practices-for-building-conversational-ai-chatbots-with-text-to-speech)
- [Top Conversational AI Platforms 2026](https://elevenlabs.io/blog/top-conversational-ai-platforms-2025)

---

## Summary of Key Recommendations

### Critical Settings

1. **Use WebRTC** (not WebSocket) for best audio quality
2. **Audio Constraints:**
   ```typescript
   {
     echoCancellation: true,
     noiseSuppression: true,
     autoGainControl: true
   }
   ```
3. **Voice Settings:**
   ```typescript
   {
     stability: 50,
     similarity: 75,
     style_exaggeration: 0
   }
   ```

### Model Selection

- **With Tools:** GPT-4o mini or Claude 3.5 Sonnet
- **Complex Reasoning:** Claude 3.7 Sonnet or Claude Sonnet 4
- **Low Latency:** Gemini Flash 2.0

### Security Essentials

- Enable conversation overrides in security settings
- Use Zero Retention Mode for sensitive data
- Implement RBAC and SSO
- Validate webhook signatures

### Performance Optimization

- Enable RAG for large knowledge bases (50% faster)
- Configure appropriate turn timeouts (1-30s)
- Use wake lock to prevent device sleep
- Monitor connection status and implement retry logic

### Token Management

- Single-use tokens expire in 15 minutes
- Refresh proactively (every 14 minutes)
- Active connections not closed on expiration
- New connections fail with expired tokens

---

**This guide is a living document. Check official ElevenLabs documentation for the latest updates and changes.**
