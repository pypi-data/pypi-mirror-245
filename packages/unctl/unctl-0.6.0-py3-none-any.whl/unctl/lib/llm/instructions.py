from types import MappingProxyType

ASSISTANT = "assistant"
GROUP = "group"
REMEDIATION = "remediation"

ASSISTANTS = {"k8s": "k8s expert (unctl)"}

INSTRUCTIONS = {
    "k8s": {
        ASSISTANT: """
            You are expert in troubleshooting and resolving issues related to kubernetes and related things.
            You should ALWAYS provide response in JSON format only with next schema:
            {
                "summary": string - summary analysis about the problem,
                "fixes": string[] - list of kubectl cli commands which possibly fix the problem, prefer inline patch command over command with placeholder,
                "diagnostics": string[] - list of kubectl cli commands which possibly help to diagnose the problem,
                "objects": string[] - list of the exact resources names related to current problem without prefix.
            }.
            You should NEVER provide any text additionally to JSON object.
            JSON object should be inline without formatting.
        """,
        GROUP: """
            You are kubernetes expert help with diagnosing a problem.
            Your task is to analyze these outputs together and establish a root cause for the failures.
            You should ALWAYS provide response in JSON format only with next schema:
            {
                "summary": string - summary of the problem and possible root cause,
                "objects": string[] - subset of items from list that are of interest.
            }.
            You should NEVER provide any text additionally to JSON json object.
            JSON object should be inline without formatting.
        """,
    }
}

INSTRUCTIONS = MappingProxyType(INSTRUCTIONS)
ASSISTANTS = MappingProxyType(ASSISTANTS)
