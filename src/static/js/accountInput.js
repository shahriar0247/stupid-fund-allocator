function AccountInput({
  index,
  step,
  enabled,
  accountName,
  accountMinSend,
  accountNameChange,
  minSendChange,
  handleEnable,
  handleDelete,
}) {
  return (
    <div
      key={index}
      className="mb-4 p-4 border rounded flex justify-between items-center"
    >
      <label className="block text-sm font-medium mb-2 dark:text-white">
        Account Name:
        <input
          type="text"
          value={accountName}
          onChange={accountNameChange}
          required
          className="py-3 px-4 block w-full border border-gray-200 rounded-lg text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none dark:bg-neutral-900 dark:border-neutral-700 dark:text-neutral-400 dark:placeholder-neutral-500 dark:focus:ring-neutral-600"
        />
      </label>

      <div className="max-w-sm space-y-3">
        <div>
          <label
            htmlFor="hs-input-with-leading-and-trailing-icon"
            className="block text-sm font-medium mb-2 dark:text-white"
          >
            Minimum Allocation:
          </label>
          <div className="relative">
            <input
              type="number"
              step={step}
              value={accountMinSend}
              onChange={minSendChange}
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
      <div class="flex">
        <label
          for="hs-default-checkbox"
          class="block font-medium dark:text-white"
        >
          Enabled:
        </label>
        <input
          type="checkbox"
          checked={enabled}
          onChange={handleEnable}
          class="shrink-0 ml-2 mt-0.5 border-gray-200 rounded text-blue-600 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none dark:bg-neutral-800 dark:border-neutral-700 dark:checked:bg-blue-500 dark:checked:border-blue-500 dark:focus:ring-offset-gray-800"
          id="hs-default-checkbox"
        />
      </div>
      <button
        type="button"
        onClick={handleDelete}
        className="w-full sm:w-auto py-3 px-4 inline-flex justify-center items-center gap-x-2 text-sm font-medium rounded-lg border border-transparent bg-red-600 text-white hover:bg-red-700 focus:outline-none focus:bg-red-700 disabled:opacity-50 disabled:pointer-events-none"
      >
        Delete
      </button>
    </div>
  );
}
