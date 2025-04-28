JOB_DEFINITION = {
    "DOCUMENT_TASK": f"Handles all actions related to individual documents or files.",
    "SELF_INTRODUCE": """Provides an introduction or detailed information about the agent when the user requests information about you. e.g. 'What can you do for me?', 'Introduce yourself', 'What can I do?' """,
    "LEARNING_TASK": [f"Handles actions where human want agent to learn from human inputs, including definition, feedback, clarification, corrections, or explanations from human inputs. The aim is to improve the agent's understanding, knowledge, or database over time through reinforcement learning, enabling it to adapt and enhance responses for future interactions.","Human express opinions, ideas, thoughts."],
    "REPLY_TASK": "Processes messages that begin with '[REPLY_TASK]', indicating that the response should follow the user's prompt exactly as specified, without any additional instructions or context.",
    "USER_PERSONA": "Manage user's profile settings or questions about user identity, e.g. asking user's name, profile; setting or modifying the user's name, preferences, or traits, and adjusts responses accordingly.",
    "AGENT_PERSONA": """Manage agent's profile settings or questions about agent identity, e.g. asking agent's name, "Who are you?", "What's your name?", profile; setting or modifying the agent's name, personality traits, or behavior. """,
    "OPENING_MSG": "Processes messages that begin with '[OPENING_MSG]:', creates greeting messages when the considering context and user preferences.",
    "SOCIAL_NETWORK": ["Handles actions and questions related to activities involving friends, social networks, communities, or groups. This includes setting or managing group notifications, integrating tools to deliver responses about recent group activities, member lists, group information, documents in the groups, time inquiries, notifications, or messaging groups.","Handles actions and questions related to social network, relationship, messages, services."],
    "ASK_QUESTION": "Handles general Q&A from the user in any language, unrelated to operations to documents, introductions, social network, relationship, messages, or expert consultations.",
    "FALLBACK_TASK": "Politely refuses requests that cannot be fulfilled or are not defined in the agent's job definitions, ensuring respectful and appropriate responses.",
}

RESPONSE_FORMAT = {
    "JOB": "[Job classification for the prompt]",
    "PROMPT": "[Input from the user]"
}