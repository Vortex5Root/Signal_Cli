# Signal-Cli Documentation

| Problem Statement | Solution |
| --- | --- |
| Signal is a popular messaging app that offers end-to-end encryption for secure communication. However, it does not provide a public API for developers to interact with the platform programmatically. This makes it difficult to automate certain tasks such as sending messages, retrieving user status, and registering new accounts. | Signal-Cli is a Python library that provides a command-line interface (CLI) for interacting with Signal Messenger. It allows you to perform various operations such as registering a new account, sending and receiving messages, and retrieving user status. This documentation provides an overview of the Signal-Cli library and its usage. |

# Introduction

This documentation provides an overview of the Signal-Cli library, which is a Python implementation for interacting with Signal Messenger using the command-line interface (CLI). Signal-Cli allows you to perform various operations such as registering a new account, sending and receiving messages, and retrieving user status.

## Dependencies

To use Signal-Cli, you need to have the following prerequisites:

- Python 3.7 or higher
- Selenium library
- GeckoDriver (Firefox driver) for Selenium

Please make sure you have these dependencies installed before proceeding.

## Index Table
| Index | Description |
| --- | --- |
| 1 | [Installation](#installation) |
| 2 | [Examples](#examples) |
| 2.1 | [Account Registration](#account-registration) |
| 2.2 | [Sending Messages](#sending-messages) |
| 2.3 | [Receiving Messages](#receiving-messages) |
| 2.4 | [Getting User Status](#getting-user-status) |
| 3 | [Class Reference](#class-reference) |
| 3.1 | [`SignalCLI`](#signalcli) |
| 3.2 | [`Message`](#message) |
| 3.3 | [`DataValidator`](#datavalidator) |
| 3.4 | [`SignalCLI_Exception`](#signalcli_exception) |
| 3.5 | [`User`](#user) |
| 4 | [Conclusion](#conclusion) |

## Installation

To install Signal-Cli, follow these steps:

1. Clone the Signal-Cli repository from GitHub:

```shell
git clone https://github.com/Vortex5Root/Signal_Cli/signal-cli.git
```
=======
poetry add git+https://github.com/Vortex5Root/Signal_Cli/signal-cli.git
```

4. Download and install GeckoDriver (Firefox driver) for Selenium. Refer to the Selenium documentation for instructions specific to your operating system.

>>>>>>> origin/main
## Examples

The following examples demonstrate how to use the Signal-Cli library for different operations.

### Account Registration

```python
import signal_cli

signal = signal_cli.SignalCLI()
signal.register('+351 929882666')
```

This example registers a new Signal account with the phone number '+351 929882666'.

### Sending Messages

```python
import signal_cli

signal = signal_cli.SignalCLI()
signal.load = '+351 929882666'  # Load the account with the specified phone number
signal.send('+351 910447343', 'Hello, this is a test message.')
```

This example sends a message from the loaded account ('+351 929882666') to the recipient '+351 910447343'.

### Receiving Messages

```python
import signal_cli

signal = signal_cli.SignalCLI()
signal.load = '+351 929882666'  # Load the account with the specified phone number
messages = signal.new_messages

for message in messages:
    msg = signal_cli.Message().load_recv(json.loads(message))
    print(f'From: {msg.from_.phone_number}')
    print(f'To: {msg.to}')
    print(f'Message: {msg.message}')
    print(f'Time Received: {msg.time_rcv}')
    print(f'Time Sent: {msg.time_send}')
```

This example retrieves and displays the received messages for the loaded account.

### Getting User Status

```python
import signal_cli

signal = signal_cli.SignalCLI()
status = signal.getUserStatus('+351 929882666')
print(status)
```

This example retrieves the status of the user with the phone number '+351 929882666'.

## Class Reference

### `SignalCLI`

The main class for interacting with Signal Messenger.

#### Properties

- `load` (getter/setter): The phone number of the loaded Signal account.

#### Methods

- `register(number: str, captcha: str = '') -> any`: Registers a new Signal account with the specified phone number and captcha.
- `send(to: str, message: str) -> list`: Sends a message to the specified recipient.
- `new_messages() -> list`: Retrieves the new messages for the loaded account.
- `getUserStatus(number: str) -> list`: Retrieves the status of the user with the specified phone number.

### `Message`

A class representing a Signal message.

#### Properties

- `from_`: The user who sent the message.
- `to_`: The recipient of the message.
- `message`: The content of the message.
- `time_rcv`: The timestamp of when the message was received.
- `time_send`: The timestamp of when the message was sent.

### `DataValidator`

A class for validating data used in Signal-Cli.

#### Methods

- `is_signal_capthe(url: str) -> bool`: Checks if the given URL is a valid Signal Captcha.
- `is_phone_number(phone: str) -> bool`: Checks if the given string is a valid phone number.

### `SignalCLI_Exception`

An exception class for Signal-Cli errors.

#### Properties

- `error_code`: A dictionary mapping error codes to error messages.

#### Methods

- `__init__(self, code, value)`: Initializes the exception with the specified error code and value.

### `User`

A class representing a Signal user.

#### Properties

- `uuid`: The UUID of the user.
- `phone_number`: The phone number of the user.
- `username`: The username of the user.

#### Methods

- `load_recv(json_values: dict) -> User`: Loads the user data from the provided JSON values.

## Author

- [Vortex5Root](https://github.com/Vortex5Root)

## Acknowledgements

- [Signal-Cli](https://github.com/AsamK/signal-cli) - The original Signal-Cli library that this documentation is based on.

## Conclusion

This documentation provided an overview of the Signal-Cli library and its usage. It covered account registration, sending and receiving messages, retrieving user status, and included a class reference for the main classes in the library. Refer to the examples and class reference for detailed usage instructions.
