$(document).ready(function() {
    // DOM Elements
    const $chatMessages = $('#chat-messages');
    const $questionInput = $('#question-input');
    const $sendBtn = $('#send-btn');
    const $resultPanel = $('#result-panel');
    const $sqlCode = $('#sql-code');
    const $answerText = $('#answer-text');
    const $closeResult = $('#close-result');
    const $loadingOverlay = $('#loading-overlay');
    const $loadingText = $('#loading-text');
    const $errorToast = $('#error-toast');
    const $errorMessage = $('#error-message');
    const $closeError = $('#close-error');

    // API Base URL
    const API_URL = '/api/chat';

    // Auto-resize textarea
    $questionInput.on('input', function() {
        this.style.height = 'auto';
        this.style.height = Math.min(this.scrollHeight, 120) + 'px';
    });

    // Handle Enter key (Shift+Enter for new line)
    $questionInput.on('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    // Send button click
    $sendBtn.on('click', sendMessage);

    // Close result panel
    $closeResult.on('click', function() {
        $resultPanel.addClass('hidden');
    });

    // Close error toast
    $closeError.on('click', function() {
        $errorToast.addClass('hidden');
    });

    // Send message function
    function sendMessage() {
        const question = $questionInput.val().trim();
        
        if (!question) {
            showError('Please enter a question');
            return;
        }

        // Add user message to chat
        addMessage(question, 'user');
        $questionInput.val('').trigger('input');
        $questionInput.prop('disabled', true);
        $sendBtn.prop('disabled', true);

        // Show loading
        showLoading('Processing your question...');

        // Make API call
        $.ajax({
            url: API_URL,
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ question: question }),
            success: function(response) {
                hideLoading();
                $questionInput.prop('disabled', false);
                $sendBtn.prop('disabled', false);
                $questionInput.focus();

                if (response.error) {
                    showError(response.error);
                    return;
                }

                // Add bot message with answer
                addMessage(response.answer, 'bot');

                // Show result panel with SQL
                showResult(response.sql, response.answer);
            },
            error: function(xhr, status, error) {
                hideLoading();
                $questionInput.prop('disabled', false);
                $sendBtn.prop('disabled', false);

                let errorMessage = 'An error occurred. Please try again.';
                if (xhr.responseJSON && xhr.responseJSON.detail) {
                    errorMessage = xhr.responseJSON.detail;
                } else if (xhr.status === 0) {
                    errorMessage = 'Cannot connect to server. Please make sure the API is running.';
                }

                showError(errorMessage);
            }
        });
    }

    // Add message to chat
    function addMessage(content, type) {
        const $messageDiv = $('<div>')
            .addClass('message')
            .addClass(type === 'user' ? 'user-message' : 'bot-message');

        const $contentDiv = $('<div>')
            .addClass('message-content');

        // Format content
        if (type === 'bot' && typeof content === 'string') {
            // Check if content contains HTML elements
            if (content.includes('<ul>') || content.includes('<li>')) {
                $contentDiv.html(content);
            } else {
                // Escape HTML and convert newlines to <br>
                const escaped = $('<div>').text(content).html();
                $contentDiv.html(escaped.replace(/\n/g, '<br>'));
            }
        } else {
            const escaped = $('<div>').text(content).html();
            $contentDiv.html(escaped.replace(/\n/g, '<br>'));
        }

        $messageDiv.append($contentDiv);
        $chatMessages.append($messageDiv);

        // Scroll to bottom
        $chatMessages.scrollTop($chatMessages[0].scrollHeight);
    }

    // Show result panel
    function showResult(sql, answer) {
        $sqlCode.text(sql);
        $answerText.text(answer);
        $resultPanel.removeClass('hidden');
    }

    // Show loading overlay
    function showLoading(text) {
        $loadingText.text(text);
        $loadingOverlay.removeClass('hidden');
    }

    // Hide loading overlay
    function hideLoading() {
        $loadingOverlay.addClass('hidden');
    }

    // Show error toast
    function showError(message) {
        $errorMessage.text(message);
        $errorToast.removeClass('hidden');

        // Auto-hide after 5 seconds
        setTimeout(function() {
            $errorToast.addClass('hidden');
        }, 5000);
    }

    // Focus input on load
    $questionInput.focus();
});
