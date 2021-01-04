import React from "react";
import { render, unmountComponentAtNode } from "react-dom";
import { act } from "react-dom/test-utils";
import { LabResponse } from "../../models/LabResponse";
import { LabService } from "../../services/LabService";
import { clickOn, flushPromises } from "../../utils/testing/TestUtils";
import LabList from "./LabsList";

let container: HTMLDivElement;
beforeEach(() => {
  // setup a DOM element as a render target
  container = document.createElement("div");
  document.body.appendChild(container);
});

afterEach(() => {
  // cleanup on exiting
  unmountComponentAtNode(container);
  container.remove();
  // container = undefined;
});

jest.mock('../../services/LabService');
const mockedLabService = LabService as jest.Mock<LabService>;
jest.mock('./LabModal', () => {
  return function DummyModal(props: { lab_id: string }) {
    return (<div className="lab-modal">{props.lab_id}</div>)
  }
})

describe("Lab List Component", () => {

  afterEach(() => {
    mockedLabService.mockClear();
  })

  it("renders lab list", async () => {
    const labs: LabResponse[] = [
      { id: 'SUPER LAB' } as LabResponse,
      { id: 'LAB FIRST' } as LabResponse,
      { id: 'KATHARA LAB' } as LabResponse
    ];

    mockedLabService.mockImplementation(() => ({
      getAllLabs: () => Promise.resolve(labs)
    }) as any);
  
    await act(async () => {
      render(<LabList />, container);
    });
    
    const cards = container.querySelectorAll('.lab-card');
    expect(cards.length).toBe(3);
  
    expect(cards[0].textContent).toContain('SUPER LAB');
    expect(cards[1].textContent).toContain('LAB FIRST');
    expect(cards[2].textContent).toContain('KATHARA LAB');
  });

  it("display correct pill", async () => {
    const labs: LabResponse[] = [
      { id: 'SUPER LAB', status: 'PREPARING' } as LabResponse,
      { id: 'LAB FIRST', status: 'RUNNING' } as LabResponse,
      { id: 'KATHARA LAB', status: 'SETUP_ERROR' } as LabResponse
    ];

    mockedLabService.mockImplementation(() => ({
      getAllLabs: () => Promise.resolve(labs)
    }) as any);
  
    await act(async () => {
      render(<LabList />, container);
    });
    
    const cards = container.querySelectorAll('.badge');
    expect(cards.length).toBe(3);
  
    expect(cards[0].textContent).toContain('Preparing');
    expect(cards[1].textContent).toContain('Running');
    expect(cards[2].textContent).toContain('Setup error');
  });

  it("display spinner while loading", async () => {
    const labs: LabResponse[] = [
      { id: 'SUPER LAB', status: 'PREPARING' } as LabResponse,
      { id: 'LAB FIRST', status: 'RUNNING' } as LabResponse,
      { id: 'KATHARA LAB', status: 'SETUP_ERROR' } as LabResponse
    ];

    let promiseNxt: (value: LabResponse[]) => void = () => {};
    const labsPromise = new Promise<LabResponse[]>((nxt, _) => {
      promiseNxt = nxt;
    });

    mockedLabService.mockImplementation(() => ({
      getAllLabs: () => labsPromise
    }) as any);
  
    await act(async () => {
      render(<LabList />, container);
    });
    
    let spinner = container.querySelector('.custom-spinner');
    expect(spinner).not.toBeNull();
  
    await act(async () => {
      promiseNxt(labs);
      await flushPromises();  
    });
    
    spinner = container.querySelector('.custom-spinner');
    expect(spinner).toBeNull();
  });

  it("display modal on clicking lab", async () => {
    const labs: LabResponse[] = [
      { id: 'SUPER LAB', status: 'PREPARING' } as LabResponse,
      { id: 'LAB FIRST', status: 'RUNNING' } as LabResponse,
      { id: 'KATHARA LAB', status: 'SETUP_ERROR' } as LabResponse
    ];

    mockedLabService.mockImplementation(() => ({
      getAllLabs: () => Promise.resolve(labs)
    }) as any);
  
    await act(async () => {
      render(<LabList />, container);
    });
    
    let modal = container.querySelector('.lab-modal');
    expect(modal).toBeNull();
    
    const cards = container.querySelectorAll('.lab-card');
    const configButton = cards[1].querySelector('.lab-config-button') as HTMLElement;

    act(() => {
      clickOn(configButton);
    });

    modal = container.querySelector('.lab-modal');
    expect(modal).not.toBeNull();
  });
});
