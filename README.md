# LLM API Caller Ansible Role

This Ansible role provides a flexible and robust way to interact with Language Model (LLM) APIs, such as [InstructLabs's](https://github.com/instructlab) LLMs. It handles API key management, dynamic model selection, and error handling.

## Features

- Dynamic model selection if not explicitly specified
- Graceful handling of missing API keys
- Error handling for API requests

## Requirements

- Ansible 2.9 or higher
- `ansible.builtin` collection

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `llm_url` | `"http://localhost:8000/v1"` | Base URL for the InstructLab LLM API |
| `llm_api_key` | `""` | API key for authentication (required for some API, not InstructLab) |
| `llm_model` | `undefined` | LLM model to use (if undefined, will be dynamically selected) |
| `llm_prompt` | `undefined` | The prompt to send to the LLM (required) |

## Example Playbook

```yaml
- hosts: localhost
  vars:
    llm_api_key: "your-api-key-here"
    llm_prompt: "Tell me a joke about Ansible"
  roles:
    - llm_caller
```

## Usage

1. Include this role in your playbook.
2. Set the required variables.
3. The role will make the API call and store the result in the `llm_result` variable.

## Error Handling

- If `llm_api_key` is not set, the role will set it to an empty string and skip API calls.
- API call failures will cause the task to fail and display an error message.

## Customization

You can customize the behavior of this role by overriding the default variables. For example, to use a different API URL or change the timeout settings:

```yaml
- hosts: localhost
  vars:
    llm_url: "https://api.alternativellm.com/v1"
  roles:
    - llm_caller
```

## Security Considerations

- Never commit your API key to version control. Use Ansible Vault or environment variables to securely manage your API key.

## Contributing

Feel free to submit issues or pull requests if you find any bugs or have suggestions for improvements.

## License

[![License](https://img.shields.io/badge/license-GPLv3-blue.svg)](https://github.com/emorisse/ansible_llm/blob/main/LICENSE)