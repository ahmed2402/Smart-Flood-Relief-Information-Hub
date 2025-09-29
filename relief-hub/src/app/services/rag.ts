import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { QueryResponse } from '../interfaces/query'; // Adjust path if necessary

@Injectable({
  providedIn: 'root'
})
export class RagService {
  private apiUrl = 'http://localhost:8000'; // Your FastAPI backend URL

  constructor(private http: HttpClient) { }

  query(question: string): Observable<QueryResponse> {
    return this.http.post<QueryResponse>(`${this.apiUrl}/query`, { query: question });
  }

  healthCheck(): Observable<any> {
    return this.http.get(`${this.apiUrl}/health`);
  }
}