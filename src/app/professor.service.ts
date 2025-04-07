import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Professor {
  id: number;
  name: string;
  title: string;
  department: string;
}

@Injectable({
  providedIn: 'root'
})
export class ProfessorService {
  // Replace the URL with your actual API endpoint if needed
  private apiUrl = 'http://127.0.0.1:5000/professors';

  constructor(private http: HttpClient) {}

  getProfessors(): Observable<Professor[]> {
    return this.http.get<Professor[]>(this.apiUrl);
  }

  getProfessor(id: number): Observable<Professor> {
    return this.http.get<Professor>(`${this.apiUrl}/${id}`);
  }

  addProfessor(professor: Professor): Observable<Professor> {
    return this.http.post<Professor>(this.apiUrl, professor);
  }

  updateProfessor(professor: Professor): Observable<any> {
    return this.http.put(`${this.apiUrl}/${professor.id}`, professor);
  }

  deleteProfessor(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/${id}`);
  }
}
