import { TestBed } from '@angular/core/testing';

import { SpinnereventsService } from './spinnerevents.service';

describe('SpinnereventsService', () => {
  let service: SpinnereventsService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(SpinnereventsService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
