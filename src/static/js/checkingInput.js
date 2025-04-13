function CheckingInput({ step, value, onChange }) {
  return (
    <div className="max-w-sm space-y-3">
      <div>
        <label
          htmlFor="hs-input-with-leading-and-trailing-icon"
          className="block text-sm font-medium mb-2 dark:text-white"
        >
          Enter money received in checking account:
        </label>
        <div className="relative">
          <input
            type="number"
            step={step}
            value={value}
            onChange={onChange}
            required
            id="hs-input-with-leading-and-trailing-icon"
            name="hs-input-with-leading-and-trailing-icon"
            className="border py-3 px-4 ps-9 pe-16 block w-full border-gray-200 shadow-sm rounded-lg text-sm focus:z-10 focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none dark:bg-neutral-900 dark:border-neutral-700 dark:text-neutral-400 dark:placeholder-neutral-500 dark:focus:ring-neutral-600"
            placeholder="0.00"
          />
          <div className="absolute inset-y-0 start-0 flex items-center pointer-events-none z-20 ps-4">
            <span className="text-gray-500 dark:text-neutral-500">$</span>
          </div>
          <div className="absolute inset-y-0 end-0 flex items-center pointer-events-none z-20 pe-4">
            <span className="text-gray-500 dark:text-neutral-500">USD</span>
          </div>
        </div>
      </div>
    </div>
  );
}
