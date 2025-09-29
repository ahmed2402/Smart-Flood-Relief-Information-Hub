import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ChatComponent } from './chat/chat';

@Component({
  selector: 'app-root',
  standalone: true, 
  imports: [CommonModule, ChatComponent],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class AppComponent {
  title = 'relief-hub';
}
