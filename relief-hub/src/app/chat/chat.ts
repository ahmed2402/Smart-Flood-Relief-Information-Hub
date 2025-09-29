import { Component, ElementRef, ViewChild, AfterViewChecked } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RagService } from '../services/rag';
import { QueryResponse } from '../interfaces/query';

interface Message {
  text: string;
  isUser: boolean;
  context?: string[];
}

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './chat.html',
  styleUrl: './chat.css',
})
export class ChatComponent implements AfterViewChecked {
  @ViewChild('messageContainer') private messageContainer!: ElementRef;

  messages: Message[] = [];
  currentQuestion: string = '';
  loading: boolean = false;

  constructor(private ragService: RagService) {
    this.addBotMessage('Hello! How can I help you find flood relief information today?');
  }

  ngAfterViewChecked(): void {
    this.scrollToBottom();
  }

  scrollToBottom(): void {
    try {
      this.messageContainer.nativeElement.scrollTop = this.messageContainer.nativeElement.scrollHeight;
    } catch (err) { }
  }

  sendMessage(): void {
    if (!this.currentQuestion.trim() || this.loading) {
      return;
    }

    const userMessage = this.currentQuestion;
    this.addUserMessage(userMessage);
    this.currentQuestion = '';
    this.loading = true;

    this.ragService.query(userMessage).subscribe({
      next: (response: QueryResponse) => {
        this.addBotMessage(response.answer, response.context);
        this.loading = false;
      },
      error: (error) => {
        console.error('Error querying RAG:', error);
        this.addBotMessage('Sorry, I encountered an error. Please try again later.');
        this.loading = false;
      }
    });
  }

  addUserMessage(text: string): void {
    this.messages.push({ text, isUser: true });
  }

  addBotMessage(text: string, context?: string[]): void {
    this.messages.push({ text, isUser: false, context });
  }

  formatBotMessage(text: string): string {
    if (!text) return '';
    // Bold: **text** => <strong>text</strong>
    let html = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    // Numbered list: 1. => <br><b>1.</b>
    html = html.replace(/(\d+)\.\s/g, '<br><b>$1.</b> ');
    // Newlines to <br>
    html = html.replace(/\n/g, '<br>');
    return html;
  }
}