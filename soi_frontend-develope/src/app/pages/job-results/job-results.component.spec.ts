import { ComponentFixture, TestBed } from '@angular/core/testing';

import { JobResultsComponent } from './job-results.component';

describe('JobResultsComponent', () => {
  let component: JobResultsComponent;
  let fixture: ComponentFixture<JobResultsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ JobResultsComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(JobResultsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
