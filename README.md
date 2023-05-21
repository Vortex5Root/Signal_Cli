# Signal-Cli Documentation

This documentation provides an overview of the Signal-Cli library, which is a Python implementation for interacting with Signal Messenger using the command-line interface (CLI). Signal-Cli allows you to perform various operations such as registering a new account, sending and receiving messages, and retrieving user status.

## Usage

To use Signal-Cli, you need to have the following prerequisites:

- Python 3.7 or higher
- Selenium library
- GeckoDriver (Firefox driver) for Selenium

Please make sure you have these dependencies installed before proceeding.

## Installation

To install Signal-Cli, follow these steps:

1. Clone the Signal-Cli repository from GitHub:

```shell
git clone https://github.com/Vortex5Root/Signal_Cli/signal-cli.git
```

2. Navigate to the Signal-Cli directory:

```shell
cd signal-cli
```

3. Install the required Python packages:

```shell
pip install -r requirements.txt
```

4. Download and install GeckoDriver (Firefox driver) for Selenium. Refer to the Selenium documentation for instructions specific to your operating system.

## Examples

The following examples demonstrate how to use the Signal-Cli library for different operations.

### Account Registration

```python
import signal_cli

signal = signal_cli.SignalCLI()
signal.register('+351 919771555')
```

This example registers a new Signal account with the phone number '+351 919771555'.

### Sending Messages

```python
import signal_cli

signal = signal_cli.SignalCLI()
signal.load = '+351 919771555'  # Load the account with the specified phone number
signal.send('+351 910456357', 'Hello, this is a test message.')
```

This example sends a message from the loaded account ('+351 919771555') to the recipient '+351 910456357'.

### Receiving Messages

```python
import signal_cli

signal = signal_cli.SignalCLI()
signal.load = '+351 919771555'  # Load the account with the specified phone number
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
status = signal.getUserStatus('+351 919771555')
print(status)
```

This example retrieves the status of the user with the phone number '+351 919771555'.

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

## Conclusion

This documentation provided an overview of the Signal-Cli library and its usage. It covered account registration, sending and receiving messages, retrieving user status, and included a class reference for the main classes in the library. Refer to the examples and class reference for detailed usage instructions.
